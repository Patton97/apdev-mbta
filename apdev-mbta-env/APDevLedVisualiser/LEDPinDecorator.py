from __future__ import annotations

from APDevLedVisualiser.LEDPin import LEDPin

class LEDPinDecorator(object):
    onColour = 'black'
    offColour = 'black'

    onRadius = 0
    offRadius = 0

    def decorate(self:LEDPinDecorator, pinToDecorate:LEDPin):
        pinToDecorate.onColour = self.onColour
        pinToDecorate.offColour = self.offColour

        pinToDecorate.onRadius = self.onRadius
        pinToDecorate.offRadius = self.offRadius