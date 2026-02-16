from __future__ import annotations
from dataclasses import dataclass

from .SoftwareLEDLine import SoftwareLEDLine

@dataclass(frozen=True)
class ImmutableSoftwareLEDLineDecoratorConfig(object):
    colour:str = None

class SoftwareLEDLineDecorator(object):
    __config:ImmutableSoftwareLEDLineDecoratorConfig

    def __init__(self:SoftwareLEDLineDecorator, config:ImmutableSoftwareLEDLineDecoratorConfig):
        self.__config = config

    def decorate(self:SoftwareLEDLineDecorator, lineToDecorate:SoftwareLEDLine):
        lineToDecorate.colour = self.__config.colour

    def decorateAll(self:SoftwareLEDLineDecorator, linesToDecorate:list[SoftwareLEDLine]):
        for lineToDecorate in linesToDecorate:
            self.decorate(lineToDecorate)