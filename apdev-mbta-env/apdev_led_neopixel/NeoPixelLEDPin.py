from __future__ import annotations

import neopixel

class NeoPixelLEDPin():

    def __init__(self:NeoPixelLEDPin, ledStrip:neopixel.NeoPixel, pinIndex:int):
        super().__init__()

        self.__onColour:list[int] = (0,0,0)
        self.__offColour:list[int] = (0,0,0)
        
        self._isLit:bool = False
        self.__isFlashing:bool = False

        self.__ledStrip:neopixel.NeoPixel = ledStrip
        self.__pinIndex:int = pinIndex

    def renderTick(self:NeoPixelLEDPin):
        self.__ledStrip[self.__pinIndex] = self.__getColour()

    def setOnColour(self:NeoPixelLEDPin, onColour:list[int]):
        self.__onColour = onColour

    def setOffColour(self:NeoPixelLEDPin, offColour:list[int]):
        self.__offColour = offColour

    def setIsFlashing(self:NeoPixelLEDPin, isFlashing:bool):
        self.__isFlashing = isFlashing

    def getIsFlashing(self:NeoPixelLEDPin) -> bool:
        return self.__isFlashing

    def __getColour(self:NeoPixelLEDPin) -> list[int]:
        if self._isLit:
            return self.__onColour
        return self.__offColour