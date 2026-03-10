from __future__ import annotations
from dataclasses import dataclass
import math

import pygame

from .SceneObject import SceneObject
from .Component import Component

from .LabelPlacement import LabelPlacement

@dataclass(frozen=True)
class ImmutableLabelPlacementData(object):
    relative_position:float
    anchor_name:str
    rotation_deg:float

class LabelComponent(Component):

    def __init__(self:LabelComponent, labelPlacement:LabelPlacement, labelText:str, ownerSize:pygame.Vector2):
        super().__init__()
        self.__labelPlacement = labelPlacement
        self.__labelText = labelText
        self.__ownerSize = ownerSize
        self.__textSurface = self.__createTextSurface()

    def renderTick(self:LabelComponent, owner:SceneObject, screen:pygame.Surface):
        super().renderTick(owner, screen)
        self.__renderLabel(owner, screen)

    def __createTextSurface(self:LabelComponent) -> pygame.Surface:
        font = pygame.font.Font('freesansbold.ttf', 12)
        return font.render(self.__labelText, True, 'white')

    def __renderLabel(self:LabelComponent, owner:SceneObject, screen:pygame.Surface):
        MARGIN:int = 4

        labelRenderPosition:pygame.Vector2 = owner.getRenderPosition(screen)
        rect:pygame.Rect = None
        pivot:pygame.Vector2 = pygame.Vector2(0,0)

        if self.__labelPlacement == LabelPlacement.NONE:
            return

        placementData = self.__getLabelPlacementData(self.__textSurface.get_rect(), MARGIN, self.__labelPlacement)

        # Apply offset
        labelRenderPosition += placementData.relative_position

        # Build rect using dynamic anchor
        rect = self.__textSurface.get_rect(**{placementData.anchor_name: labelRenderPosition})

        # Extract pivot
        pivot = pygame.Vector2(*getattr(rect, placementData.anchor_name))

        dx = rect.center[0] - pivot.x
        dy = rect.center[1] - pivot.y
        rotAngleRad = math.radians(placementData.rotation_deg)

        rotatedCentre = pygame.Vector2(
            pivot.x + dx * math.cos(rotAngleRad) - dy * math.sin(rotAngleRad),
            pivot.y + dx * math.sin(rotAngleRad) + dy * math.cos(rotAngleRad)
        )

        textSurface = pygame.transform.rotate(self.__textSurface, -placementData.rotation_deg)
        rect = textSurface.get_rect(center=(rotatedCentre.x, rotatedCentre.y))

        screen.blit(textSurface, rect)

    def __getLabelPlacementData(self:LabelComponent, textRect:pygame.Rect, margin:int, labelPlacement:LabelPlacement) -> ImmutableLabelPlacementData:
        match labelPlacement:
            case LabelPlacement.TOP_LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__ownerSize.x, -self.__ownerSize.y),
                    "midright",
                    45
                )

            case LabelPlacement.TOP:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        -(textRect.height / 2) - self.__ownerSize.y - margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.TOP_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.__ownerSize.x, -self.__ownerSize.y),
                    "midleft",
                    -45
                )

            case LabelPlacement.LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__ownerSize.x - margin, 0),
                    "midright",
                    0
                )

            case LabelPlacement.CENTRE:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-textRect.width / 2, 0),
                    "center",
                    0
                )

            case LabelPlacement.RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.__ownerSize.x + margin, 0),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__ownerSize.x, self.__ownerSize.y),
                    "midright",
                    -45
                )

            case LabelPlacement.BOTTOM:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        (textRect.height / 2) + self.__ownerSize.y + margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.__ownerSize.x, self.__ownerSize.y),
                    "midleft",
                    45
                )
            
        return None