from __future__ import annotations

from abc import ABC, abstractmethod

from apdev_led.ILEDPinController import ILEDPinController

class BaseLEDPinController(ILEDPinController):

    @abstractmethod
    def get_is_lit(self:BaseLEDPinController) -> bool:
        pass

    @abstractmethod
    def set_is_lit(self:BaseLEDPinController, is_lit:bool):
        pass

    def toggle_is_lit(self:BaseLEDPinController) -> bool:
        wasLit = self.get_is_lit()
        newIsList = not wasLit
        self.set_is_lit(newIsList)
        return newIsList