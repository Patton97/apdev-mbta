from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from .Component import Component

@dataclass(frozen=True)
class ImmutableAnimationStage(object):
    enterDelegate:Callable[[None], None]
    updateDelegate:Callable[[float], None]
    lengthInMilliseconds:int

class AnimationComponent(Component):

    def __init__(self:AnimationComponent, animationStages:list[ImmutableAnimationStage]):
        super().__init__()
        self.__timeUntilNextAnimationStage:int = 0
        self.__animationStages:list[ImmutableAnimationStage]
        self.__currentAnimationStage = 0
        self.__animationStages = animationStages
        self.__setAnimationStage(0)

    def updateTick(self:AnimationComponent, dt:float):
        self.__timeUntilNextAnimationStage -= dt
        if self.__timeUntilNextAnimationStage <= 0:
            self.__incrementAnimationStage()
            
        updateDelegate = self.__animationStages[self.__currentAnimationStage].updateDelegate
        if updateDelegate is not None:
            updateDelegate(dt)

    def resetAnimation(self:AnimationComponent):
        self.__setAnimationStage(0)

    def __incrementAnimationStage(self:AnimationComponent):
        self.__setAnimationStage(self.__currentAnimationStage + 1)

    def __setAnimationStage(self:AnimationComponent, index:int):
        # wrap back to 0 if over end
        if index >= len(self.__animationStages):
            index = 0

        self.__currentAnimationStage = index

        currentAnimationStage:ImmutableAnimationStage = self.__animationStages[self.__currentAnimationStage]

        self.__timeUntilNextAnimationStage = currentAnimationStage.lengthInMilliseconds

        # tell the animation stage it has been entered
        if currentAnimationStage.enterDelegate is not None:
            currentAnimationStage.enterDelegate()