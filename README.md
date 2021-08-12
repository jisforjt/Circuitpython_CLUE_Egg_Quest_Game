# Circuitpython_CLUE_Egg_Quest_Game
This game was designed to be used with the Adafruit's CLUE and Yahboom's gamepad. It

![Image of Egg Quest Game Cover](https://github.com/jisforjt/Circuitpython_CLUE_Egg_Quest_Game/blob/main/images/Egg_Quest.PNG)
This is a higher-level library to allow Adafruit's [CLUE](https://www.adafruit.com/product/4500) and Yahboom's Micro:bit Compact [Gamepad](http://www.yahboom.net/study/SGH) to communicate while maintaining all the functionality of the CLUE, except for touch features.

## Dependencies
This library depends on:
* [Adafruit CircuitPython](https://github.com/adafruit/circuitpython) v.6.3.0
* [Adafruit_CLUE**](https://github.com/adafruit/Adafruit_CircuitPython_CLUE) v.3.0.0
* [JisforJT Yahboom Gamepad](https://github.com/jisforjt/CircuitPython_CLUE_Yahboom_Gamepad) v.1.0.0
* [Adafruit Imangeload**](https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad) v.1.15.1
* [Adafruit Display Text**](https://github.com/adafruit/Adafruit_CircuitPython_Display_Text) v.2.20.0

**Repository is available in the Circuitpython Bundle v.6.X


## Instalations
Follow Adafruit's [CLUE Overview](https://learn.adafruit.com/adafruit-clue) instructions under _CircuitPython on CLUE_. During the installation process, you will download the latest _library bundle_ and transfer several libraries to the CLUE. Also transfer the dependencies listed above to your _lib folder_.
Download this repository and copy _main.py_, _jisforjt_egg_quest.py_, and _jt_sprites.bmp_ on to your CIRCUITPY drive.

## Directory
```
CIRCUITPY
|-lib (folder)
|-main.py
|-jisforjt_egg_quest.py
|-jt_sprites.bmp
```


## Usage
You can create a new main.py file and use:
```python
from jisforjt_yahboom_gamepad import gamepad
```

## License
The code of the repository is made available under the terms of the MIT license. See license.md for more information.
