from __future__ import annotations

from ..ILEDPinController import ILEDPinController
from .SoftwareLEDPin import SoftwareLEDPin

class SoftwareLEDPinController(ILEDPinController):
    __controlledPin:SoftwareLEDPin

    def takeControlOf(self:SoftwareLEDPinController, pinToControl:SoftwareLEDPin):
        self.__controlledPin = pinToControl
    
    def get_is_lit(self:SoftwareLEDPinController) -> bool:
        return self.__controlledPin.isLit
    
    def set_is_lit(self, is_lit):
        self.__controlledPin.isLit = is_lit

    def toggle_is_lit(self):
        wasLit = self.__controlledPin.isLit
        self.__controlledPin.isLit = not wasLit
        return not wasLit