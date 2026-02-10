from __future__ import annotations

import pygame

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin

class SoftwareLEDPinFactory(object):

    def createAllPins(
        self:SoftwareLEDPinFactory,
        stop_metadata_list:list[ImmutableStopMetadata],
        screenMargin:pygame.Vector2,
        pinGridScale:int) -> dict[str, SoftwareLEDPin]:

        pinsKeyedByStationID:dict[str, SoftwareLEDPin] = dict[str,  SoftwareLEDPin]()
        for stop_metadata in stop_metadata_list:
            pinsKeyedByStationID[stop_metadata.id] = self.__createPin(
                stop_metadata,
                screenMargin,
                pinGridScale
            )

        return pinsKeyedByStationID

    def __createPin(self:SoftwareLEDPinFactory,
        stop_metadata:ImmutableStopMetadata,
        screenMargin:pygame.Vector2,
        pinGridScale:int) -> SoftwareLEDPin:

        pin = SoftwareLEDPin()
        pin.label = stop_metadata.name
        pin.gridPosition = pygame.Vector2(
            stop_metadata.standardised_location_x,
            stop_metadata.standardised_location_y
        )
        pin.gridScale = pinGridScale
        pin.screenMargin = screenMargin
        pin.labelPlacement = stop_metadata.label_placement
        pin.isFlashing = True

        return pin