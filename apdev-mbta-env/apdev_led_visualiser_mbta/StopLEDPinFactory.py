from __future__ import annotations

import pygame

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

from apdev_led_visualiser.LEDPin import LEDPin

class StopLEDPinFactory(object):

    def createAllPins(
        self:StopLEDPinFactory,
        stop_metadata_list:list[ImmutableStopMetadata],
        pinGridScale:int) -> dict[str, LEDPin]:

        pinsKeyedByStationID:dict[str, LEDPin] = dict[str,  LEDPin]()
        for stop_metadata in stop_metadata_list:
            pinsKeyedByStationID[stop_metadata.id] = self.__createPin(
                stop_metadata,
                pinGridScale
            )

        return pinsKeyedByStationID

    def __createPin(
        self:StopLEDPinFactory,
        stop_metadata:ImmutableStopMetadata,
        pinGridScale:int) -> LEDPin:

        pin = LEDPin()
        pin.setGridPosition(pygame.Vector2(
            stop_metadata.standardised_location_x,
            stop_metadata.standardised_location_y
        ))
        pin.setGridScale(pinGridScale)

        return pin