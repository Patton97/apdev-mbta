from __future__ import annotations

import pygame

from .Component import Component

class SceneObject(object):
    def __init__(self:SceneObject):
        self.__components:list[Component] = []
        self.__gridPosition:pygame.Vector2 = pygame.Vector2(0,0)
        self.__gridScale:int = 1

    def updateTick(self:SceneObject, dt:float):
        for component in self.__components:
            component.updateTick(dt)

    def renderTick(self:SceneObject, screen:pygame.Surface):
        for component in self.__components:
            component.renderTick(self, screen)

    def addComponent(self:SceneObject, component:Component):
        self.__components.append(component)

    def removeComponent(self:SceneObject, component:Component):
        self.__components.remove(component)

    def getGridPosition(self:SceneObject) -> pygame.Vector2:
        return self.__gridPosition

    def setGridPosition(self:SceneObject, gridPosition:pygame.Vector2):
        self.__gridPosition = gridPosition

    def getGridScale(self:SceneObject) -> pygame.Vector2:
        return self.__gridScale

    def setGridScale(self:SceneObject, gridScale:int):
        self.__gridScale = gridScale

    def getRenderPosition(self:SceneObject, screen:pygame.Surface) -> pygame.Vector2:
        return pygame.Vector2(
            self.__gridPosition.x * self.__gridScale,
            screen.get_size()[1] - self.__gridPosition.y * self.__gridScale
        )