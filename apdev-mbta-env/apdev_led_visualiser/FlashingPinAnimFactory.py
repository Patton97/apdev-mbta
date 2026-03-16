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
        enterStage0 = lambda: self.__turnOff(pin)
        enterStage1 = lambda: self.__turnOn(pin)
        updateStage1 = lambda dt: self.__updateOnLED(pin, dt)

        return AnimationComponent([
            ImmutableAnimationStage(enterStage0, None, self.__offLengthInMilliseconds),
            ImmutableAnimationStage(enterStage1, updateStage1, self.__onLengthInMilliseconds),
        ])

    def __turnOff(self:FlashingPinAnimFactory, pin:LEDPin):
        pin._setIsLit(False)

    def __turnOn(self:FlashingPinAnimFactory, pin:LEDPin):
        if pin.getIsFlashing():
            pin._setIsLit(True)

    def __updateOnLED(self:FlashingPinAnimFactory, pin:LEDPin, dt:float):
        if not pin.getIsFlashing():
            pin.__currentColourIndex = 0
            pin.__colours.clear()
            return
        
        # TODO AP: Figure out some sort of index selection based on delta time
        
        