from __future__ import annotations

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin

from apdev_led_visualiser.AnimationComponent import AnimationComponent, ImmutableAnimationStage

class SoftwareLEDPinFlashingAnimationComponentFactory(object):
    def __init__(
        self:SoftwareLEDPinFlashingAnimationComponentFactory,
        offLengthInMilliseconds:int,
        onLengthInMilliseconds:int):
    
        self.__offLengthInMilliseconds = offLengthInMilliseconds
        self.__onLengthInMilliseconds = onLengthInMilliseconds

    def create(self:SoftwareLEDPinFlashingAnimationComponentFactory, pin:SoftwareLEDPin):

        stage0 = lambda: pin._setIsLit(False)
        stage1 = lambda: pin._setIsLit(True)
        return AnimationComponent([
            ImmutableAnimationStage(stage0, None, self.__offLengthInMilliseconds),
            ImmutableAnimationStage(stage1, None, self.__onLengthInMilliseconds),
        ])