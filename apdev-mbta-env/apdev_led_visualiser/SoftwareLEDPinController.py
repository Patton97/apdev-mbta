from __future__ import annotations

from ILEDPinController import ILEDPinController
from .SoftwareLEDPin import SoftwareLEDPin

class SoftwareLEDPinController(ILEDPinController):
    __controlledPin:SoftwareLEDPin
    def __init__(self:SoftwareLEDPinController, pinToControl:SoftwareLEDPin):
        self.__controlledPin = pinToControl
    
    def get_is_lit(self:SoftwareLEDPinController) -> bool:
        return self.__controlledPin.isFlashing
    
    def set_is_lit(self, is_lit):
        self.__controlledPin.isFlashing = is_lit

    def toggle_is_lit(self):
        wasLit = self.__controlledPin.isFlashing
        self.__controlledPin.isFlashing = not wasLit
        return not wasLit