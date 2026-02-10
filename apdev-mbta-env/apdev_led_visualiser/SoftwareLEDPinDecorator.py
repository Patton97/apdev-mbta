from __future__ import annotations
from dataclasses import dataclass

from .SoftwareLEDPin import SoftwareLEDPin

@dataclass(frozen=True)
class ImmutableSoftwareLEDPinDecoratorConfig(object):
    onColour:str = None
    offColour:str = None
    onRadius:int = 0
    offRadius:int = 0

class SoftwareLEDPinDecorator(object):
    __config:ImmutableSoftwareLEDPinDecoratorConfig

    def __init__(self:SoftwareLEDPinDecorator, config:ImmutableSoftwareLEDPinDecoratorConfig):
        self.__config = config

    def decorate(self:SoftwareLEDPinDecorator, pinToDecorate:SoftwareLEDPin):
        pinToDecorate.onColour = self.__config.onColour
        pinToDecorate.offColour = self.__config.offColour

        pinToDecorate.onRadius = self.__config.onRadius
        pinToDecorate.offRadius = self.__config.offRadius

    def decorateAll(self:SoftwareLEDPinDecorator, pinsToDecorate:list[SoftwareLEDPin]):
        for pinToDecorate in pinsToDecorate:
            self.decorate(pinToDecorate)