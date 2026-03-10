from __future__ import annotations

import pygame

from apdev_pygame_engine.SceneObject import SceneObject

class LEDPin(SceneObject):

    def __init__(self:LEDPin):
        super().__init__()

        self.__onColour:str = 'black'
        self.__offColour:str = 'black'

        self.__onRadius:int = 0
        self.__offRadius:int = 0
        
        self.__isLit:bool = False
        self.__isFlashing:bool = False

    def renderTick(self:LEDPin, screen:pygame.Surface):
        super().renderTick(screen)
        self.__renderPin(screen)

    def setOnColour(self:LEDPin, onColour:str):
        self.__onColour = onColour

    def setOffColour(self:LEDPin, offColour:str):
        self.__offColour = offColour

    def setOnRadius(self:LEDPin, onRadius:int):
        self.__onRadius = onRadius

    def setOffRadius(self:LEDPin, offRadius:int):
        self.__offRadius = offRadius

    def setIsFlashing(self:LEDPin, isFlashing:bool):
        self.__isFlashing = isFlashing

    def getIsFlashing(self:LEDPin) -> bool:
        return self.__isFlashing

    def _setIsLit(self:LEDPin, isLit:bool):
        self.__isLit = isLit

    def __getColour(self:LEDPin) -> str:
        if self.__isLit:
            return self.__onColour
        return self.__offColour

    def __getRadius(self:LEDPin) -> int:
        if self.__isLit:
            return self.__onRadius
        return self.__offRadius

    def __renderPin(self:LEDPin, screen:pygame.Surface):
        pygame.draw.circle(screen, self.__getColour(), self.getRenderPosition(screen), self.__getRadius())