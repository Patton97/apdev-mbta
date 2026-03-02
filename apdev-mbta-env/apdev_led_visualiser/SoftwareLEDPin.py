from __future__ import annotations

import pygame

from .SceneObject import SceneObject

class SoftwareLEDPin(SceneObject):

    def __init__(self:SoftwareLEDPin):
        super().__init__()

        self.__onColour:str = 'black'
        self.__offColour:str = 'black'

        self.__onRadius:int = 0
        self.__offRadius:int = 0
        
        self.__isLit:bool = False
        self.__isFlashing:bool = False

    def renderTick(self:SoftwareLEDPin, screen:pygame.Surface):
        super().renderTick(screen)
        self.__renderPin(screen)

    def setOnColour(self:SoftwareLEDPin, onColour:str):
        self.__onColour = onColour

    def setOffColour(self:SoftwareLEDPin, offColour:str):
        self.__offColour = offColour

    def setOnRadius(self:SoftwareLEDPin, onRadius:int):
        self.__onRadius = onRadius

    def setOffRadius(self:SoftwareLEDPin, offRadius:int):
        self.__offRadius = offRadius

    def setIsFlashing(self:SoftwareLEDPin, isFlashing:bool):
        self.__isFlashing = isFlashing

    def getIsFlashing(self:SoftwareLEDPin) -> bool:
        return self.__isFlashing

    def _setIsLit(self:SoftwareLEDPin, isLit:bool):
        self.__isLit = isLit

    def __getColour(self:SoftwareLEDPin) -> str:
        if self.__isLit:
            return self.__onColour
        return self.__offColour

    def __getRadius(self:SoftwareLEDPin) -> int:
        if self.__isLit:
            return self.__onRadius
        return self.__offRadius

    def __renderPin(self:SoftwareLEDPin, screen:pygame.Surface):
        pygame.draw.circle(screen, self.__getColour(), self.getRenderPosition(screen), self.__getRadius())