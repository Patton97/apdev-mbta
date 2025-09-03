from __future__ import annotations

import pygame

from .LEDPin import LEDPin

class LEDVisualiser(object):
    def start(self:LEDVisualiser):
        self.loop()

    def loop(self:LEDVisualiser):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True

        MAX_FPS = 60

        pin = LEDPin()
        pin.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        pin.onColour = 'chartreuse'
        pin.offColour = 'chartreuse4'
        pin.onRadius = 10
        pin.offRadius = 8

        deltaTime = 1 / MAX_FPS * 1000
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill('black')

            pin.updateTick(deltaTime)
            pin.renderTick(screen)

            pygame.display.flip()

            deltaTime = clock.tick(MAX_FPS)

        pygame.quit()
        return