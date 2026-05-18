from __future__ import annotations

from apdev_led.BaseLEDPinController import BaseLEDPinController

from apdev_led_neopixel.NeoPixelLEDPin import NeoPixelLEDPin

class NeoPixelLEDPinController(BaseLEDPinController):

    def __init__(self:NeoPixelLEDPinController, pinToControl:NeoPixelLEDPin):
        self.__pinToControl:NeoPixelLEDPin = pinToControl
    
    def get_is_lit(self:NeoPixelLEDPinController) -> bool:
        return self.__pinToControl.getIsFlashing()
    
    def set_is_lit(self, is_lit):
        self.__pinToControl.setIsFlashing(is_lit)