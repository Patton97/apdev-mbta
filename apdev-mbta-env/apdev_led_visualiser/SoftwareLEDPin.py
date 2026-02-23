from __future__ import annotations
from dataclasses import dataclass

import math
from typing import Tuple

import pygame

from .SceneObject import SceneObject
from .AnimationComponent import AnimationComponent, ImmutableAnimationStage

from apdev_mbta_data.LabelPlacement import LabelPlacement

@dataclass(frozen=True)
class ImmutableLabelPlacementData(object):
    relative_position:float
    anchor_name:str
    rotation_deg:float

class SoftwareLEDPin(SceneObject):    

    def __init__(self:SoftwareLEDPin):
        super().__init__()

        self.__gridPosition:pygame.Vector2 = pygame.Vector2(0,0)
        self.__gridScale:int = 1

        self.__labelText:str = 'label'
        
        self.__onColour:str = 'black'
        self.__offColour:str = 'black'

        self.__onRadius:int = 0
        self.__offRadius:int = 0

        self.__labelPlacement:LabelPlacement = LabelPlacement.NONE
        
        self.__isLit:bool = True

        animationComponent = AnimationComponent([
            ImmutableAnimationStage(self.__configureAnimationStage0, None, 1000),
            ImmutableAnimationStage(self.__configureAnimationStage1, None, 2000),
        ])
        self.addComponent(animationComponent)

    def renderTick(self:SoftwareLEDPin, screen:pygame.Surface):
        self.__renderPin(screen)        
        self.__renderLabel(screen)

    def setGridPosition(self:SoftwareLEDPin, gridPosition:pygame.Vector2):
        self.__gridPosition = gridPosition

    def setGridScale(self:SoftwareLEDPin, gridScale:int):
        self.__gridScale = gridScale

    def setLabelText(self:SoftwareLEDPin, labelText:str):
        self.__labelText = labelText

    def setOnColour(self:SoftwareLEDPin, onColour:str):
        self.__onColour = onColour

    def setOffColour(self:SoftwareLEDPin, offColour:str):
        self.__offColour = offColour

    def setOnRadius(self:SoftwareLEDPin, onRadius:int):
        self.__onRadius = onRadius

    def setOffRadius(self:SoftwareLEDPin, offRadius:int):
        self.__offRadius = offRadius

    def setLabelPlacement(self:SoftwareLEDPin, labelPlacement:LabelPlacement):
        self.__labelPlacement = labelPlacement

    def startFlashing(self:SoftwareLEDPin):
        self.__isFlashing = True

    def startFlashing(self:SoftwareLEDPin):
        self.__isFlashing = False

    def __getColour(self:SoftwareLEDPin) -> str:
        if self.__isLit:
            return self.__onColour
        return self.__offColour
    
    def __getRadius(self:SoftwareLEDPin) -> int:
        if self.__isLit:
            return self.__onRadius
        return self.__offRadius
    
    def __getRenderPosition(self:SoftwareLEDPin, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.__gridPosition.x * self.__gridScale,
            screenSize.y - self.__gridPosition.y * self.__gridScale
        )
    
    def __renderPin(self:SoftwareLEDPin, screen:pygame.Surface):
        pygame.draw.circle(screen, self.__getColour(), self.__getRenderPosition(screen), self.__getRadius())
    
    def __renderLabel(self:SoftwareLEDPin, screen:pygame.Surface):
        MARGIN:int = 4
        font = pygame.font.Font('freesansbold.ttf', 12)
        textSurface = font.render(self.__labelText, True, 'white')
        textRect = textSurface.get_rect()        

        labelRenderPosition:pygame.Vector2 = self.__getRenderPosition(screen)
        rect:pygame.Rect = None
        pivot:pygame.Vector2 = pygame.Vector2(0,0)

        if self.__labelPlacement == LabelPlacement.NONE:
            return

        placementData = self.__getLabelPlacementData(textRect, MARGIN, self.__labelPlacement)

        # Apply offset
        labelRenderPosition += placementData.relative_position

        # Build rect using dynamic anchor
        rect = textSurface.get_rect(**{placementData.anchor_name: labelRenderPosition})

        # Extract pivot
        pivot = pygame.Vector2(*getattr(rect, placementData.anchor_name))

        dx = rect.center[0] - pivot.x
        dy = rect.center[1] - pivot.y
        rotAngleRad = math.radians(placementData.rotation_deg)

        rotatedCentre = pygame.Vector2(
            pivot.x + dx * math.cos(rotAngleRad) - dy * math.sin(rotAngleRad),
            pivot.y + dx * math.sin(rotAngleRad) + dy * math.cos(rotAngleRad)
        )

        textSurface = pygame.transform.rotate(textSurface, -placementData.rotation_deg)
        rect = textSurface.get_rect(center=(rotatedCentre.x, rotatedCentre.y))

        screen.blit(textSurface, rect)

    def __getLabelPlacementData(self:SoftwareLEDPin, textRect:pygame.Rect, margin:int, labelPlacement:LabelPlacement) -> ImmutableLabelPlacementData:
        match labelPlacement:
            case LabelPlacement.TOP_LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__onRadius, -self.__onRadius),
                    "midright",
                    45
                )

            case LabelPlacement.TOP:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        -(textRect.height / 2) - self.__onRadius - margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.TOP_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.__onRadius, -self.__onRadius),
                    "midleft",
                    -45
                )

            case LabelPlacement.LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__onRadius - margin, 0),
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
                    pygame.Vector2(self.__onRadius + margin, 0),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.__onRadius, self.__onRadius),
                    "midright",
                    -45
                )

            case LabelPlacement.BOTTOM:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        (textRect.height / 2) + self.__onRadius + margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.__onRadius, self.__onRadius),
                    "midleft",
                    45
                )
            
        return None

    def __configureAnimationStage0(self:SoftwareLEDPin):
        self.__isLit = False

    def __configureAnimationStage1(self:SoftwareLEDPin):
        self.__isLit = True