from __future__ import annotations

import pygame

from .SceneObject import SceneObject

class LEDVisualiser(object):

    def __init__(self:LEDVisualiser):
        pygame.init()
        self.__objects:list[SceneObject] = []
        self.__screen:pygame.Surface = None

    def getScreenSize(self:LEDVisualiser) -> pygame.Vector2:
        currentSize = pygame.display.get_window_size()
        return pygame.Vector2(currentSize[0], currentSize[1])

    def setScreenSize(self:LEDVisualiser, width:int, height:int, newIsFullscreen:bool):
        self.__screen = pygame.display.set_mode((width, height))

        if newIsFullscreen:
            self.__screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            self.__screen = pygame.display.set_mode((width, height))

    def setFullscreen(self:LEDVisualiser, newIsFullscreen:bool):
        currentSize = pygame.display.get_window_size()
        self.setScreenSize(currentSize[0], currentSize[1], newIsFullscreen)

    def addToCanvas(self:LEDVisualiser, objectToAdd):
        self.__objects.append(objectToAdd)

    def start(self:LEDVisualiser):
        self.__loop()

    def __loop(self:LEDVisualiser):
        clock = pygame.time.Clock()
        running = True

        MAX_FPS = 60
        deltaTime = 1 / MAX_FPS * 1000
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.__screen.fill('black')

            for object in self.__objects:
                object.updateTick(deltaTime)
                object.renderTick(self.__screen)

            pygame.display.flip()

            deltaTime = clock.tick(MAX_FPS)

        pygame.quit()
        return