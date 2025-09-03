from __future__ import annotations

import pygame

from .LEDPin import LEDPin
from .LEDPinDecorator import LEDPinDecorator

class LEDVisualiser(object):
    def start(self:LEDVisualiser):
        self.loop()

    def loop(self:LEDVisualiser):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True

        MAX_FPS = 60

        greenLinePinDecorator = LEDPinDecorator()
        greenLinePinDecorator.onColour = 'chartreuse'
        greenLinePinDecorator.offColour = 'chartreuse4'
        greenLinePinDecorator.onRadius = 10
        greenLinePinDecorator.offRadius = 8

        pinPositions = [pygame.Vector2(50, 670), pygame.Vector2(75, 645)]
        pins:list[LEDPin] = []

        for pinPosition in pinPositions:
            pin = LEDPin()
            pin.position = pinPosition
            greenLinePinDecorator.decorate(pin)
            pins.append(pin)

        deltaTime = 1 / MAX_FPS * 1000
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill('black')

            for pin in pins:
                pin.updateTick(deltaTime)
                pin.renderTick(screen)

            pygame.display.flip()

            deltaTime = clock.tick(MAX_FPS)

        pygame.quit()
        return