from __future__ import annotations
from dataclasses import dataclass

from .SoftwareLEDLine import SoftwareLEDLine

@dataclass(frozen=True)
class ImmutableSoftwareLEDLineDecoratorConfig(object):
    colour:str = None

class SoftwareLEDLineDecorator(object):
    def __init__(self:SoftwareLEDLineDecorator, config:ImmutableSoftwareLEDLineDecoratorConfig):
        self.__config:ImmutableSoftwareLEDLineDecoratorConfig = config

    def decorate(self:SoftwareLEDLineDecorator, lineToDecorate:SoftwareLEDLine):
        lineToDecorate.setColour(self.__config.colour)

    def decorateAll(self:SoftwareLEDLineDecorator, linesToDecorate:list[SoftwareLEDLine]):
        for lineToDecorate in linesToDecorate:
            self.decorate(lineToDecorate)