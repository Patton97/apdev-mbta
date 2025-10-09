from __future__ import annotations

import pygame

class SoftwareLEDPin(object):
    position:str = pygame.Vector2(0,0)
    onColour:str = 'black'
    offColour = 'black'

    onRadius = 0
    offRadius = 0

    label = 'label'

    isLit:bool = False

    timeUntilNextAnimationStage = 0

    def configureAnimationStage0(self:SoftwareLEDPin, dt:float):
        self.colour = self.offColour
        self.radius = self.offRadius

    def configureAnimationStage1(self:SoftwareLEDPin, dt:float):
        self.colour = self.onColour
        self.radius = self.onRadius

    animationStageConfigureDelegates = [configureAnimationStage0, configureAnimationStage1]
    animationStageLengthsInMilliseconds = [1000, 2000]
    currentAnimationStage = 0

    def resetAnimation(self:SoftwareLEDPin):
        self.currentAnimationStage = 0
        self.timeUntilNextAnimationStage = 0

    def updateAnimation(self:SoftwareLEDPin, dt:float):
        self.timeUntilNextAnimationStage -= dt
        if self.timeUntilNextAnimationStage <= 0:
            self.currentAnimationStage += 1
            if self.currentAnimationStage >= len(self.animationStageConfigureDelegates):
                self.currentAnimationStage = 0
            self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[self.currentAnimationStage]
        
        self.animationStageConfigureDelegates[self.currentAnimationStage](self, dt)

    def updateTick(self:SoftwareLEDPin, dt:float):
        # if not lit, ensure anim props are reset
        if not self.isLit:
            self.resetAnimation()
            return

        self.updateAnimation(dt)

    def renderTick(self:SoftwareLEDPin, screen:pygame.Surface):        
        pygame.draw.circle(screen, self.colour, self.position, self.radius)
        text = pygame.font.Font('freesansbold.ttf', 12).render(self.label, True, 'white')
        screen.blit(text, pygame.rect.Rect(self.position.x + self.onRadius + 4, self.position.y - self.onRadius/2, 0,0))