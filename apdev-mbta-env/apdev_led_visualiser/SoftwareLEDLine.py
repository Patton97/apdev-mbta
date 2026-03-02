from __future__ import annotations

from typing import Tuple

import pygame

from .SceneObject import SceneObject

class SoftwareLEDLine(SceneObject):

    def __init__(self:SoftwareLEDLine):
        self.__gridStartPosition:pygame.Vector2 = pygame.Vector2(0,0)
        self.__gridEndPosition:pygame.Vector2 = pygame.Vector2(0,0)
        self.__gridScale:int = 1        
        self.__width:int = 10
        self.__colour:str = 'black'

    def updateTick(self:SoftwareLEDLine, dt:int):
        pass

    def renderTick(self:SoftwareLEDLine, screen:pygame.Surface):
        self.__render(screen)
    
    def getColour(self:SoftwareLEDLine) -> str:
        return self.__colour
    
    def setColour(self:SoftwareLEDLine, colour:str):
        self.__colour = colour

    def setGridStartPosition(self:SoftwareLEDLine, gridStartPosition:pygame.Vector2):
        self.__gridStartPosition = gridStartPosition

    def setGridEndPosition(self:SoftwareLEDLine, gridEndPosition:pygame.Vector2):
        self.__gridEndPosition = gridEndPosition

    def setGridScale(self:SoftwareLEDLine, gridScale:int):
        self.__gridScale = gridScale
    
    def __getStartRenderPosition(self:SoftwareLEDLine, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.__gridStartPosition.x * self.__gridScale,
            screenSize.y - self.__gridStartPosition.y * self.__gridScale
        )
    
    def __getEndRenderPosition(self:SoftwareLEDLine, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.__gridEndPosition.x * self.__gridScale,
            screenSize.y - self.__gridEndPosition.y * self.__gridScale
        )
    
    def __renderLine(self:SoftwareLEDLine, screen:pygame.Surface):
        pygame.draw.line(
            screen,
            self.getColour(),
            self.__getStartRenderPosition(screen),
            self.__getEndRenderPosition(screen),
            self.__width
        )

    def __renderJointCircle(self:SoftwareLEDLine, screen:pygame.Surface, renderPosition:pygame.Vector2):
        pygame.draw.circle(
            screen,
            self.getColour(),
            renderPosition,
            self.__width / 3
        )
    
    def __render(self:SoftwareLEDLine, screen:pygame.Surface):
        self.__renderLine(screen)
        self.__renderJointCircle(screen, self.__getStartRenderPosition(screen))
        self.__renderJointCircle(screen, self.__getEndRenderPosition(screen))