from __future__ import annotations

import pygame

class LEDPin(object):
    position = pygame.Vector2(0,0)
    onColour = 'black'
    offColour = 'black'

    onRadius = 0
    offRadius = 0

    timeUntilNextAnimationStage = 0

    def configureAnimationStage0(self:LEDPin, dt:float):
        self.colour = self.offColour
        self.radius = self.offRadius

    def configureAnimationStage1(self:LEDPin, dt:float):
        self.colour = self.onColour
        self.radius = self.onRadius

    animationStageConfigureDelegates = [configureAnimationStage0, configureAnimationStage1]
    animationStageLengthsInMilliseconds = [1000, 2000]
    currentAnimationStage = 0

    def updateTick(self:LEDPin, dt:float):
        self.timeUntilNextAnimationStage -= dt
        if self.timeUntilNextAnimationStage <= 0:
            self.currentAnimationStage += 1
            if self.currentAnimationStage >= len(self.animationStageConfigureDelegates):
                self.currentAnimationStage = 0
            self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[self.currentAnimationStage]
        
        self.animationStageConfigureDelegates[self.currentAnimationStage](self, dt)

    def renderTick(self:LEDPin, screen:pygame.Surface):        
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
        return