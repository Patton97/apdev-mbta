from __future__ import annotations

from apdev_pygame_engine.AnimationComponent import AnimationComponent, ImmutableAnimationStage

from .LEDPin import LEDPin

class FlashingPinAnimFactory(object):
    def __init__(
        self:FlashingPinAnimFactory,
        offLengthInMilliseconds:int,
        onLengthInMilliseconds:int):
    
        self.__offLengthInMilliseconds = offLengthInMilliseconds
        self.__onLengthInMilliseconds = onLengthInMilliseconds

    def create(self:FlashingPinAnimFactory, pin:LEDPin):
        stage0 = lambda: self.__turnOff(pin)
        stage1 = lambda: self.__turnOn(pin)
        return AnimationComponent([
            ImmutableAnimationStage(stage0, None, self.__offLengthInMilliseconds),
            ImmutableAnimationStage(stage1, None, self.__onLengthInMilliseconds),
        ])

    def __turnOff(self:FlashingPinAnimFactory, pin:LEDPin):
        pin._setIsLit(False)

    def __turnOn(self:FlashingPinAnimFactory, pin:LEDPin):
        if pin.getIsFlashing():
            pin._setIsLit(True)