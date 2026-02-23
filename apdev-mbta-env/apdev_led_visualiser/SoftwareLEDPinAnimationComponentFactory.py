from __future__ import annotations

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin

from apdev_led_visualiser.AnimationComponent import AnimationComponent, ImmutableAnimationStage

class SoftwareLEDPinAnimationComponentFactory(object):
    def createFlashingAnimationComponent(
            self:SoftwareLEDPinAnimationComponentFactory,
            pin:SoftwareLEDPin,
            offLengthInMilliseconds:int,
            onLengthInMilliseconds:int):
        stage0 = lambda: pin._setIsLit(False)
        stage1 = lambda: pin._setIsLit(True)
        return AnimationComponent([
            ImmutableAnimationStage(stage0, None, offLengthInMilliseconds),
            ImmutableAnimationStage(stage1, None, onLengthInMilliseconds),
        ])