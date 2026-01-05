from __future__ import annotations
from dataclasses import dataclass

import math
from typing import Tuple

import pygame

from apdev_mbta_data.LabelPlacement import LabelPlacement

@dataclass(frozen=True)
class ImmutableLabelPlacementData(object):
    relative_position:float
    anchor_name:str
    rotation_deg:float

class SoftwareLEDPin(object):
    gridPosition:pygame.Vector2 = pygame.Vector2(0,0)
    gridScale:int = 1
    screenMargin:pygame.Vector2 = pygame.Vector2(0,0)

    label:str = 'label'
    isFlashing:bool = False
    isLit:bool = False
    
    onColour:str = 'black'
    offColour:str = 'black'

    onRadius:int = 0
    offRadius:int = 0

    labelPlacement:LabelPlacement 

    timeUntilNextAnimationStage:int = 0

    def updateTick(self:SoftwareLEDPin, dt:float):
        # if not flashing, ensure anim props are reset
        if not self.isFlashing:
            self.__resetAnimation()
        
        self.__updateAnimation(dt)

    def renderTick(self:SoftwareLEDPin, screen:pygame.Surface):
        self.__renderPin(screen)        
        self.__renderLabel(screen)

    def __getColour(self:SoftwareLEDPin) -> str:
        if self.isLit:
            return self.onColour
        return self.offColour
    
    def __getRadius(self:SoftwareLEDPin) -> int:
        if self.isLit:
            return self.onRadius
        return self.offRadius
    
    def __getRenderPosition(self:SoftwareLEDPin, screen:pygame.Surface) -> pygame.Vector2:
        screenSize:Tuple[int,int] = screen.get_size()
        screenSize:pygame.Vector2 = pygame.Vector2(screenSize[0], screenSize[1])

        return pygame.Vector2(
            self.gridPosition.x * self.gridScale,
            screenSize.y - self.gridPosition.y * self.gridScale
        )
    
    def __renderPin(self:SoftwareLEDPin, screen:pygame.Surface):
        pygame.draw.circle(screen, self.__getColour(), self.__getRenderPosition(screen), self.__getRadius())
    
    def __renderLabel(self:SoftwareLEDPin, screen:pygame.Surface):
        MARGIN:int = 4
        font = pygame.font.Font('freesansbold.ttf', 12)
        textSurface = font.render(self.label, True, 'white')
        textRect = textSurface.get_rect()        

        labelRenderPosition:pygame.Vector2 = self.__getRenderPosition(screen)
        rect:pygame.Rect = None
        pivot:pygame.Vector2 = pygame.Vector2(0,0)

        if self.labelPlacement == LabelPlacement.NONE:
            return

        placementData = self.__getLabelPlacementData(textRect, MARGIN, self.labelPlacement)

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
                    pygame.Vector2(-self.onRadius, -self.onRadius),
                    "midright",
                    45
                )

            case LabelPlacement.TOP:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        -(textRect.height / 2) - self.onRadius - margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.TOP_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.onRadius, -self.onRadius),
                    "midleft",
                    -45
                )

            case LabelPlacement.LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.onRadius - margin, 0),
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
                    pygame.Vector2(self.onRadius + margin, 0),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_LEFT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(-self.onRadius, self.onRadius),
                    "midright",
                    -45
                )

            case LabelPlacement.BOTTOM:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(
                        -textRect.width / 2,
                        (textRect.height / 2) + self.onRadius + margin
                    ),
                    "midleft",
                    0
                )

            case LabelPlacement.BOTTOM_RIGHT:
                return ImmutableLabelPlacementData(
                    pygame.Vector2(self.onRadius, self.onRadius),
                    "midleft",
                    45
                )
            
        return None

    def __configureAnimationStage0(self:SoftwareLEDPin, dt:float):
        self.isLit = False

    def __configureAnimationStage1(self:SoftwareLEDPin, dt:float):
        self.isLit = True

    animationStageConfigureDelegates = [__configureAnimationStage0, __configureAnimationStage1]
    animationStageLengthsInMilliseconds = [1000, 2000]
    currentAnimationStage = 0

    def __resetAnimation(self:SoftwareLEDPin):
        self.currentAnimationStage = 0
        self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[0]

    def __updateAnimation(self:SoftwareLEDPin, dt:float):
        self.timeUntilNextAnimationStage -= dt
        if self.timeUntilNextAnimationStage <= 0:
            self.currentAnimationStage += 1
            if self.currentAnimationStage >= len(self.animationStageConfigureDelegates):
                self.currentAnimationStage = 0
            self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[self.currentAnimationStage]

        self.animationStageConfigureDelegates[self.currentAnimationStage](self, dt)