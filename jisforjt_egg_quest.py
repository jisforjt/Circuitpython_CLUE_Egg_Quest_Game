# CircuitPython Clue Yahboom Gamepad Egg Quest jisforjt_egg_quest.py
# Last Updated Aug. 10, 2021
# Author: James Tobin

######################################################
#   MIT License
######################################################
'''
Copyright (c) 2020 James Tobin
Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
'''

######################################################
#   Cutebot Information
######################################################
'''
jisforjt_egg_quest.py:
v1
    Brave adventurer, you are quested to collect as many eggs as
    you cane from the four realms. Be quick because the gate will
    close soon and once it is you will be trapped.

    This game was created to demonstrate the functionality of the
    Yahboom gamepad with the Adafurit CLUE.

    The only function that was not demonstrated was the 
    buzzer/rumbler.
'''

######################################################
#   Import
######################################################
import time
import board
import random
import displayio
import adafruit_imageload
import terminalio
from adafruit_display_text import label
from jisforjt_yahboom_gamepad import gamepad
from adafruit_clue import clue


######################################################
#   Variables
######################################################
display = clue.display      # Borrow the clue display connection
tile_size = 32              # Set tile size we are using 32 x 32
tile_center = tile_size / 2         # Calculate tile center
max_width = display.width - tile_size       # Calculate maximum width that allows us to see the whole tile
max_height = display.height - tile_size     # Calculate maximum height that allows us to see the whole tile

sprite_sheet, palette = adafruit_imageload.load("/jt_sprites.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)      #import bmp sprite sheet image.
eggs = displayio.TileGrid(sprite_sheet, pixel_shader=palette, width = 1, height = 1, tile_width = tile_size, tile_height = tile_size)           # Create grid item for eggs
player1 = displayio.TileGrid(sprite_sheet, pixel_shader=palette, width = 1, height = 1, tile_width = tile_size, tile_height = tile_size)        # Create grid item for player1
  
timer_label = label.Label(terminalio.FONT, text="Timer", color=0xFFFFFF)    # Create label for timer
score_label = label.Label(terminalio.FONT, text="Score", color=0xFFFFFF)    # Create label for score

group = displayio.Group(scale=1)    # Create display group 
group.append(eggs)      # Add the eggs grid item to the group. Items that are added first will be the background.
group.append(player1)   # Add the player1 grid item to the group. 
group.append(timer_label)   # Add timer label to the group.
group.append(score_label)   # Add score label to the group. Items that are added last will be the foreground.

# Set the position for the labels.
timer_label.x = 16
timer_label.y = 16
score_label.x = display.width - 16
score_label.y = 16

right_face = True   # Player1 state that indicates which way it faces
frame_step = False  # Player1 state that indicates which foot we are stepping with

total_score = 0     # Value that stores the total score.

paused = False      # Game state that indicates if the game is paused
game_reset = True   # Game state that indicates if the game is ready to reset

curr_realm = 0        # Stores which realm we are in
egg_carton = []     # An array that will contain all the eggs' locations

start_time = 0      # Stores when the game started
total_gameplay_time = 60    # Stores how many seconds the game will last
stop_time = 0       # Stores how much time the game has been stopped for while paused


######################################################
#   Functions
######################################################
def move(x, y):
    '''
    Controls the movements of player1
    '''
    global frame_step

    # Set player1.x location
    temp = player1.x + x
    temp = min(max(temp,0),max_width)   # Limit temp to a value between 0 and the max_width
    player1.x = temp

    # Set player1.y location
    temp = player1.y + y
    temp = min(max(temp,0), max_height)     # Limit temp to a value between 0 and the max_height
    player1.y = temp

    if x != 0 or y != 0:
        frame_step = not frame_step     # Change frame_step if player1 is moving

    player1[0] = 4 + (right_face * 2) + frame_step      # Set to correct tile on sprite_sheet

def collect_egg():
    '''
    Checks to see if we collected an egg
    '''
    global curr_realm, total_score
    x, y = egg_carton[curr_realm]     # Get current realm's egg location
    if x + tile_center > player1.x and x + tile_center < player1.x + tile_size:     # Check to see if the width of player1 tile is over the center of the eggs tile
        if y + tile_center > player1.y and y + tile_center < player1.y + tile_size:     # Check to see if the height of player1 tile is over the center of the eggs tile
            # Move current egg out of view
            eggs.x = int(display.width)
            eggs.y = 0

            egg_carton[curr_realm] = spawn_egg()      # Get location of new egg
            
            total_score += 1    # Increase total_score by 1

def spawn_egg():
    '''
    Sets the location of a new egg
    '''
    while True:
        # Randomly Generate an egg location within the 16 pixel buffer around the edge
        coor_x = random.randint(16, max_width-16)       
        coor_y = random.randint(16, max_height-16)

        # Check to make sure that the new egg is not spawned next to player1's current location.
        if coor_x < player1.x - (tile_size * 2) or coor_x > player1.x + (tile_size * 2):
            if coor_y < player1.y - (tile_size * 2) or coor_y > player1.y + (tile_size * 2):
                return coor_x, coor_y

def show_egg(button_number):
    '''
    Reveal the egg in the new realm. It will not show player1 a new egg for the realm it is already in until it leaves that realm.
    
    label  Number  Color  
     B1      1      red
     B2      2     green
     B3      3      blue
     B4      4     yellow
    '''
    global curr_realm
    button_number -= 1      # Convert button number to an index number

    if curr_realm != button_number:   # Compare button number to current realm index number.
        curr_realm = button_number
        eggs[0] = curr_realm          # Set correct realm's egg sprite
        eggs.x, eggs.y = egg_carton[curr_realm]       # Set eggs tile location


######################################################
#   Main Code
######################################################
# Game play instructions
print("--------------------------------")
print("--------------------------------")
print("EGG QUEST")
print(" ")
print("Brave seeker you must collect as many eggs as you can. Use the color buttons to change the realms you search in. Use the joystick to move. Press the joystick button to pause and start the game.")
print(" ")
print("Press the joystick button to start the game.")

# Wait for player to start game
while True:
    if gamepad.press == True:
        break

# Main loob
while True:
    if gamepad.press:       # Check to see if joystick button pressed
        paused = not paused     # Switch true/false value
        if paused == True:      
            stop_time = time.time()     # When paused start stop timer
        else:
            total_gameplay_time = total_gameplay_time + (time.time() - stop_time)   # When unpaused calculate time paused and add it to the total_gameplay_time
        time.sleep(0.1)     # Give the player time to release button
       
        # Set all game values to starting values
        if game_reset == True:
            paused = False
            game_reset = False

            # Set player1 location
            player1.x = int(max_width/2)
            player1.y = int(max_height/2)

            player1[0] = 0      # Set player1 sprite

            right_face = True       # Set which way player1 looks
            frame_step = False      # Set which step player1 is taking

            random.seed(int((gamepad.y_voltage + (1 + gamepad.x_voltage)) * 52))      # Use joystick voltages to seed the random number generator

            total_score = 0

            # Create the initinal locations for the eggs
            egg_carton = []
            for i in range(4):
                egg_carton.append(spawn_egg())

            curr_realm = 0      # Set starting realm
            eggs.x, eggs.y = egg_carton[curr_realm]      # Set current realm's egg location
            
            eggs[0] = curr_realm    # Set egg sprite

            # Count Down
            print("3...")
            time.sleep(0.5)
            print("2...")
            time.sleep(0.5)
            print("1...")
            time.sleep(0.5)
            print("Starting game...")

            total_gameplay_time = 60    # Set duration of game
            start_time = time.time()    # Set start time 
    
            display.show(group)         # Show game pieces

    if not paused:
        delta_x = 0
        delta_y = 0

        # Check joystick for movement. 
        # Use a 0.04 buffer to prevent manufacturing irregularities from moving player1 accidentally, i.e. 0.46 and 0.54 instead of 0.50.
        if gamepad.x > 0.54:
            delta_x = 2
            right_face = False
        elif gamepad.x < 0.46:
            delta_x = -2
            right_face = True
        if gamepad.y > 0.54:
            delta_y = 2
        elif gamepad.y < 0.46:
            delta_y = -2

        move(delta_x, delta_y)      # Move player1 by delta_x and delta_y
        collect_egg()        # Check to see if the current realm's egg has been collected

        # Check to see if the player wants to change realms.
        if gamepad.b1:
            show_egg(1)
        elif gamepad.b2:
            show_egg(2)
        elif gamepad.b3:
            show_egg(3)
        elif gamepad.b4:
            show_egg(4)

        score_label.text = str(total_score)         # Update score and convert integer to string
        curr_time = total_gameplay_time - (time.time() - start_time)        # Calculate how much time is left
        timer_label.text = str(curr_time)       # Update timer and convert integer to string
        
        # End of game
        if curr_time < 1:
            display.show(None)      # Show terminal
            print("--------------------------------")
            print("--------------------------------")
            print("You collected %i eggs!" % total_score)
            print(" ")
            print("Press the joystick button to try again for a better score!")
            paused = True       # Pause game
            game_reset = True   # Enable reset


