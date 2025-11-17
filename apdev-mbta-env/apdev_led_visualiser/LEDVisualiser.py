from __future__ import annotations

import pygame

from .SoftwareLEDPin import SoftwareLEDPin
from .SoftwareLEDPinController import SoftwareLEDPinController

class LEDVisualiser(object):
    objects:list[SoftwareLEDPin] = []
    controllersKeyedByID:dict[str, SoftwareLEDPinController] = dict[str, SoftwareLEDPinController]()

    __screen:pygame.Surface = None

    def __init__(self:LEDVisualiser):
        pygame.init()

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

    def addLEDController(self:LEDVisualiser, id:str, controllerToAdd:SoftwareLEDPinController):
        self.controllersKeyedByID[id] = controllerToAdd

    def addToCanvas(self:LEDVisualiser, objectToAdd):
        self.objects.append(objectToAdd)

    def start(self:LEDVisualiser):
        self.__loop()

    def __loop(self:LEDVisualiser):
        pygame.init()
        clock = pygame.time.Clock()
        running = True

        MAX_FPS = 60
        deltaTime = 1 / MAX_FPS * 1000
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.controllersKeyedByID["place-eliot"].set_is_lit(keys[pygame.K_e])

            self.__screen.fill('black')

            for object in self.objects:
                object.updateTick(deltaTime)
                object.renderTick(self.__screen)

            pygame.display.flip()

            deltaTime = clock.tick(MAX_FPS)

        pygame.quit()
        return