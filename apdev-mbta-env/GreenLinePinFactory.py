from __future__ import annotations

import pygame

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin
from apdev_led_visualiser.LEDPinDecorator import LEDPinDecorator

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

class GreenLinePinFactory(object):
    def createAllPins(
        self:GreenLinePinFactory,
        stop_metadata_list:list[ImmutableStopMetadata],
        screenMargin:pygame.Vector2,
        pinGridScale:int) -> dict[str, SoftwareLEDPin]:
        
        greenLinePinDecorator = LEDPinDecorator()
        greenLinePinDecorator.onColour = 'chartreuse'
        greenLinePinDecorator.offColour = 'chartreuse4'
        greenLinePinDecorator.onRadius = 10
        greenLinePinDecorator.offRadius = 8

        pinsKeyedByStationID:dict[str, SoftwareLEDPin] = dict[str,  SoftwareLEDPin]()
        for stop_metadata in stop_metadata_list:
            pinsKeyedByStationID[stop_metadata.id] = self.__createPin(
                stop_metadata,
                greenLinePinDecorator,
                screenMargin,
                pinGridScale
            )

        return pinsKeyedByStationID

    def __createPin(self:GreenLinePinFactory,
        stop_metadata:ImmutableStopMetadata,
        decorator:LEDPinDecorator,
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
        decorator.decorate(pin)
        return pin