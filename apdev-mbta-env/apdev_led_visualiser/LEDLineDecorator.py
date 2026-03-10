from __future__ import annotations
from dataclasses import dataclass

from .LEDLine import LEDLine

@dataclass(frozen=True)
class ImmutableLEDLineDecoratorConfig(object):
    colour:str = None

class LEDLineDecorator(object):
    def __init__(self:LEDLineDecorator, config:ImmutableLEDLineDecoratorConfig):
        self.__config:ImmutableLEDLineDecoratorConfig = config

    def decorate(self:LEDLineDecorator, lineToDecorate:LEDLine):
        lineToDecorate.setColour(self.__config.colour)

    def decorateAll(self:LEDLineDecorator, linesToDecorate:list[LEDLine]):
        for lineToDecorate in linesToDecorate:
            self.decorate(lineToDecorate)