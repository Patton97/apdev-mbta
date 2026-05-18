from __future__ import annotations

import neopixel

from apdev_led.BaseLEDPinController import BaseLEDPinController

class NeoPixelLEDPinController(BaseLEDPinController):

    def __init__(self:NeoPixelLEDPinController, ledStrip:neopixel.NeoPixel, pinIndex:int, pinColour:list):
        self.__ledStrip:neopixel.NeoPixel = ledStrip
        self.__pinIndex:int = pinIndex
        self.__pinColour:list = pinColour
    
    def get_is_lit(self:NeoPixelLEDPinController) -> bool:
        return self.__ledStrip[self.__pinIndex][0] != 0 or self.__ledStrip[self.__pinIndex][0] != 0 or self.__ledStrip[self.__pinIndex][2] != 0
    
    def set_is_lit(self, is_lit):
        if is_lit:
            self.__ledStrip[self.__pinIndex] = self.__pinColour
        else:
            self.__ledStrip[self.__pinIndex] = (0, 0, 0)