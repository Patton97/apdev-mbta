from __future__ import annotations

from typing import Tuple

import pygame

from .SceneObject import SceneObject

class SoftwareLEDLine(SceneObject):
    gridStartPosition:pygame.Vector2 = pygame.Vector2(0,0)
    gridEndPosition:pygame.Vector2 = pygame.Vector2(0,0)
    gridScale:int = 1
    
    width:int = 10

    colour:str = 'black'

    def updateTick(self:SoftwareLEDLine, dt:int):
        pass

    def renderTick(self:SoftwareLEDLine, screen:pygame.Surface):
        self.__render(screen)
    
    def __getColour(self:SoftwareLEDLine) -> str:
        return self.colour
    
    def __getStartRenderPosition(self:SoftwareLEDLine, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.gridStartPosition.x * self.gridScale,
            screenSize.y - self.gridStartPosition.y * self.gridScale
        )
    
    def __getEndRenderPosition(self:SoftwareLEDLine, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.gridEndPosition.x * self.gridScale,
            screenSize.y - self.gridEndPosition.y * self.gridScale
        )
    
    def __renderLine(self:SoftwareLEDLine, screen:pygame.Surface):
        pygame.draw.line(
            screen,
            self.__getColour(),
            self.__getStartRenderPosition(screen),
            self.__getEndRenderPosition(screen),
            self.width
        )

    def __renderJointCircle(self:SoftwareLEDLine, screen:pygame.Surface, renderPosition:pygame.Vector2):
        pygame.draw.circle(
            screen,
            self.__getColour(),
            renderPosition,
            self.width / 3
        )
    
    def __render(self:SoftwareLEDLine, screen:pygame.Surface):
        self.__renderLine(screen)
        self.__renderJointCircle(screen, self.__getStartRenderPosition(screen))
        self.__renderJointCircle(screen, self.__getEndRenderPosition(screen))