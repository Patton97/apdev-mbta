from __future__ import annotations
from dataclasses import dataclass

import pygame

from apdev_mbta_data.LabelPlacement import LabelPlacement

from .SoftwareLEDPin import SoftwareLEDPin
from .SoftwareLEDPinFlashingAnimationComponentFactory import SoftwareLEDPinFlashingAnimationComponentFactory
from .LabelComponent import LabelComponent

@dataclass(frozen=True)
class ImmutableSoftwareLEDPinDecoratorConfig(object):
    onColour:str = None
    offColour:str = None
    onRadius:int = 0
    offRadius:int = 0
    animComponentFactory:SoftwareLEDPinFlashingAnimationComponentFactory = None
    labelPlacement:LabelPlacement = LabelPlacement.NONE
    labelText:str = None

class SoftwareLEDPinDecorator(object):
    def decorate(self:SoftwareLEDPinDecorator, pinToDecorate:SoftwareLEDPin, config:ImmutableSoftwareLEDPinDecoratorConfig):
        pinToDecorate.setOnColour(config.onColour)
        pinToDecorate.setOffColour(config.offColour)

        pinToDecorate.setOnRadius(config.onRadius)
        pinToDecorate.setOffRadius(config.offRadius)

        if config.animComponentFactory is not None:
            animComponent = config.animComponentFactory.create(pinToDecorate)
            pinToDecorate.addComponent(animComponent)

        if config.labelPlacement is not LabelPlacement.NONE:
            labelComponent = LabelComponent(
                config.labelPlacement,
                config.labelText,
                pygame.Vector2(config.onRadius, config.onRadius)
            )
            pinToDecorate.addComponent(labelComponent)

    def decorateAll(self:SoftwareLEDPinDecorator, pinsToDecorate:list[SoftwareLEDPin]):
        for pinToDecorate in pinsToDecorate:
            self.decorate(pinToDecorate)