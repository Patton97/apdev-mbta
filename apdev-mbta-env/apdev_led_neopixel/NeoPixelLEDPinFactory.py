from __future__ import annotations

import neopixel

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

from .NeoPixelLEDPin import NeoPixelLEDPin

class NeoPixelLEDPinFactory(object):

    def createAllPins(
        self:NeoPixelLEDPinFactory,
        stop_metadata_list:list[ImmutableStopMetadata],
        strip:neopixel.NeoPixel) -> dict[str, NeoPixelLEDPin]:

        pinsKeyedByStationID:dict[str, NeoPixelLEDPin] = dict[str,  NeoPixelLEDPin]()
        for stop_metadata in stop_metadata_list:
            pinsKeyedByStationID[stop_metadata.id] = self.__createPin(
                stop_metadata,
                strip
            )

        return pinsKeyedByStationID

    def __createPin(
        self:NeoPixelLEDPinFactory,
        stop_metadata:ImmutableStopMetadata,
        strip:neopixel.NeoPixel) -> NeoPixelLEDPin:

        pin = NeoPixelLEDPin(strip, stop_metadata.pin_index)
        pin.setOnColour([127, 255, 0])
        pin.setIsFlashing(True)

        return pin