from __future__ import annotations

import pygame

from apdev_pygame_engine.SceneObject import SceneObject

MAX_FPS = 60

class LEDVisualiser(object):

    def __init__(self:LEDVisualiser):
        self.__objects:list[SceneObject] = []
        self.__screen:pygame.Surface = None
        self.__looping:bool = False

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
        if not self.__looping:
            self.__startLoop()

    def stop(self:LEDVisualiser):
        self.__looping = False

    def __startLoop(self:LEDVisualiser):
        clock = pygame.time.Clock()
        self.__looping = True

        while self.__looping:
            self.__tickLoop(clock, MAX_FPS)            

        pygame.quit()
    
    def __tickLoop(self:LEDVisualiser, clock:pygame.time.Clock, maxFPS:int):
        deltaTime = clock.tick(maxFPS)
        
        self.__processEvents()
        self.__updateAllObjects(deltaTime)

        self.__screen.fill('black')
        self.__renderAllObjects()
        pygame.display.flip()

    def __processEvents(self:LEDVisualiser):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()

    def __updateAllObjects(self:LEDVisualiser, deltaTime:int):
        for object in self.__objects:
            object.updateTick(deltaTime)

    def __renderAllObjects(self:LEDVisualiser):
        for object in self.__objects:
            object.renderTick(self.__screen)