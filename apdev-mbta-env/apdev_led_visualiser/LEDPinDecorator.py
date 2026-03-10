from __future__ import annotations
from dataclasses import dataclass

import pygame

from apdev_pygame_engine.labels.LabelPlacement import LabelPlacement
from apdev_pygame_engine.labels.LabelComponent import LabelComponent

from .LEDPin import LEDPin
from .FlashingPinAnimFactory import FlashingPinAnimFactory

@dataclass(frozen=True)
class ImmutableLEDPinDecoratorConfig(object):
    onColour:str = None
    offColour:str = None
    onRadius:int = 0
    offRadius:int = 0
    animComponentFactory:FlashingPinAnimFactory = None
    labelPlacement:LabelPlacement = LabelPlacement.NONE
    labelText:str = None

class LEDPinDecorator(object):

    def decorate(self:LEDPinDecorator, pinToDecorate:LEDPin, config:ImmutableLEDPinDecoratorConfig):
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

    def decorateAll(self:LEDPinDecorator, pinsToDecorate:list[LEDPin]):
        for pinToDecorate in pinsToDecorate:
            self.decorate(pinToDecorate)