from __future__ import annotations

import pygame

from .SoftwareLEDPin import SoftwareLEDPin

class LEDVisualiser(object):
    objects:list[SoftwareLEDPin] = []

    __screen:pygame.Surface = None

    def __init__(self):
        pygame.init()

    def setScreenSize(self:LEDVisualiser, width:int, height:int):
        self.__screen = pygame.display.set_mode((width, height))

    def addToCanvas(self:LEDVisualiser, objectToAdd):
        self.objects.append(objectToAdd)

    def start(self:LEDVisualiser):
        self.loop()

    def loop(self:LEDVisualiser):
        pygame.init()
        clock = pygame.time.Clock()
        running = True

        MAX_FPS = 60
        deltaTime = 1 / MAX_FPS * 1000
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.__screen.fill('black')

            for object in self.objects:
                object.updateTick(deltaTime)
                object.renderTick(self.__screen)

            pygame.display.flip()

            deltaTime = clock.tick(MAX_FPS)

        pygame.quit()
        return