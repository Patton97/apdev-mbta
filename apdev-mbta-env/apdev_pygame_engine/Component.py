from __future__ import annotations

import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .SceneObject import SceneObject

class Component(object):
    def updateTick(self:Component, dt:float):
        pass

    def renderTick(self:Component, owner:SceneObject, screen:pygame.Surface):
        pass