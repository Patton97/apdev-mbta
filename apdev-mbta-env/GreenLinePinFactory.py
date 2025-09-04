from __future__ import annotations

import pygame

from APDevLEDVisualiser.LEDPin import LEDPin
from APDevLEDVisualiser.LEDPinDecorator import LEDPinDecorator

class GreenLinePinFactory(object):
    def createAllPins(
        self:GreenLinePinFactory,
        screenSize:pygame.Vector2,
        screenMargin:pygame.Vector2,
        adjacentPinMargin:int) -> list[LEDPin]:
        
        greenLinePinDecorator = LEDPinDecorator()
        greenLinePinDecorator.onColour = 'chartreuse'
        greenLinePinDecorator.offColour = 'chartreuse4'
        greenLinePinDecorator.onRadius = 10
        greenLinePinDecorator.offRadius = 8

        stationNames = self.__getStationNames()
        pins:list[LEDPin] = [self.__createPin(stationNames[i], greenLinePinDecorator) for i in range(len(stationNames))]

        # riverside to fenway
        for i in range(13):
            x = screenMargin.x + i * adjacentPinMargin
            y = screenSize.y - screenMargin.y - i * adjacentPinMargin
            pins[i].position = pygame.Vector2(x, y)
        return pins

    def __createPin(self:GreenLinePinFactory, label:str, decorator:LEDPinDecorator) -> LEDPin:
        pin = LEDPin()
        pin.label = label
        decorator.decorate(pin)
        return pin

    def __getStationNames(self:GreenLinePinFactory):
        return [
            "Riverside",
            "Woodland",
            "Waban",
            "Eliot",
            "Newton Highlands",
            "Newton Centre",
            "Chestnut Hill",
            "Reservoir",
            "Beaconsfield",
            "Brookline Hills",
            "Brookline Village",
            "Longwood",
            "Fenway",
            "Kenmore",
            "Hynes Convention Centre",
            "Copley",
            "Arlington",
            "Boylston",
            "Park Street",
            "Government Centre",
            "North Station",
            "Science Park/West End",
            "Lechmere",
            "Union Square"
        ]
