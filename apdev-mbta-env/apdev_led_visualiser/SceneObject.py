from __future__ import annotations

import pygame

class SceneObject(object):

    def updateTick(self:SceneObject, dt:float):
        pass

    def renderTick(self:SceneObject, screen:pygame.Surface):
        pass