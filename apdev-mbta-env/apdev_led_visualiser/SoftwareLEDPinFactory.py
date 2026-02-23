from __future__ import annotations

import pygame

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin

class SoftwareLEDPinFactory(object):

    def createAllPins(
        self:SoftwareLEDPinFactory,
        stop_metadata_list:list[ImmutableStopMetadata],
        pinGridScale:int) -> dict[str, SoftwareLEDPin]:

        pinsKeyedByStationID:dict[str, SoftwareLEDPin] = dict[str,  SoftwareLEDPin]()
        for stop_metadata in stop_metadata_list:
            pinsKeyedByStationID[stop_metadata.id] = self.__createPin(
                stop_metadata,
                pinGridScale
            )

        return pinsKeyedByStationID

    def __createPin(
        self:SoftwareLEDPinFactory,
        stop_metadata:ImmutableStopMetadata,
        pinGridScale:int) -> SoftwareLEDPin:

        pin = SoftwareLEDPin()
        pin.setLabelText(stop_metadata.name)
        pin.setGridPosition(pygame.Vector2(
            stop_metadata.standardised_location_x,
            stop_metadata.standardised_location_y
        ))
        pin.setGridScale(pinGridScale)
        pin.setLabelPlacement(stop_metadata.label_placement)
        pin.setOnRadius(10)
        pin.setOffRadius(8)
        pin.setOnColour(stop_metadata.primary_colour)
        pin.setOffColour(stop_metadata.secondary_colour)
        pin.startFlashing()

        return pin