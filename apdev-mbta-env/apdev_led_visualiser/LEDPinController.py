from __future__ import annotations

from apdev_led.ILEDPinController import ILEDPinController
from .LEDPin import LEDPin

class LEDPinController(ILEDPinController):

    def __init__(self:LEDPinController, pinToControl:LEDPin):
        self.__controlledPin:LEDPin = pinToControl
    
    def get_is_lit(self:LEDPinController) -> bool:
        return self.__controlledPin.getIsFlashing()
    
    def set_is_lit(self:LEDPinController, is_lit:bool):
        self.__controlledPin.setIsFlashing(is_lit)

    def toggle_is_lit(self:LEDPinController):
        wasLit = self.__controlledPin.getIsFlashing()
        newIsList = not wasLit
        self.__controlledPin.setIsFlashing(newIsList)
        return newIsList
    
    def set_colours(self:LEDPinController, colours:list[str]):
        self.__controlledPin.setColours(colours)