from __future__ import annotations

import pygame

from apdev_led_visualiser.Component import Component

class SceneObject(object):
    def __init__(self:SceneObject):
        self.__components:list[Component] = []

    def updateTick(self:SceneObject, dt:float):
        for component in self.__components:
            component.updateTick(dt)

    def renderTick(self:SceneObject, screen:pygame.Surface):
        pass

    def addComponent(self:SceneObject, component:Component):
        self.__components.append(component)

    def removeComponent(self:SceneObject, component:Component):
        self.__components.remove(component)