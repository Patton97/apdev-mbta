from __future__ import annotations
from dataclasses import dataclass

from .SoftwareLEDPin import SoftwareLEDPin

from apdev_led_visualiser.SoftwareLEDPinAnimationComponentFactory import SoftwareLEDPinAnimationComponentFactory

@dataclass(frozen=True)
class ImmutableSoftwareLEDPinDecoratorConfig(object):
    onColour:str = None
    offColour:str = None
    onRadius:int = 0
    offRadius:int = 0
    animComponentFactory:SoftwareLEDPinAnimationComponentFactory = None
    offLengthInMilliseconds:int = 0
    onLengthInMilliseconds:int = 0

class SoftwareLEDPinDecorator(object):
    __config:ImmutableSoftwareLEDPinDecoratorConfig

    def __init__(self:SoftwareLEDPinDecorator, config:ImmutableSoftwareLEDPinDecoratorConfig):
        self.__config = config

    def decorate(self:SoftwareLEDPinDecorator, pinToDecorate:SoftwareLEDPin):
        pinToDecorate.setOnColour(self.__config.onColour)
        pinToDecorate.setOffColour(self.__config.offColour)

        pinToDecorate.setOnRadius(self.__config.onRadius)
        pinToDecorate.setOffRadius(self.__config.offRadius)
        if self.__config.animComponentFactory is not None:
            animComponent = self.__config.animComponentFactory.createFlashingAnimationComponent(
                pinToDecorate,
                self.__config.offLengthInMilliseconds,
                self.__config.onLengthInMilliseconds
            )
            pinToDecorate.addComponent(animComponent)

    def decorateAll(self:SoftwareLEDPinDecorator, pinsToDecorate:list[SoftwareLEDPin]):
        for pinToDecorate in pinsToDecorate:
            self.decorate(pinToDecorate)