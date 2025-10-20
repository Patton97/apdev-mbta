from __future__ import annotations

import pygame

class SoftwareLEDPin(object):
    position:str = pygame.Vector2(0,0)
    label:str = 'label'
    isFlashing:bool = False
    isLit:bool = False
    
    onColour:str = 'black'
    offColour:str = 'black'

    onRadius:int = 0
    offRadius:int = 0

    timeUntilNextAnimationStage:int = 0

    def __getColour(self:SoftwareLEDPin) -> str:
        if self.isLit:
            return self.onColour
        return self.offColour
    
    def __getRadius(self:SoftwareLEDPin) -> int:
        if self.isLit:
            return self.onRadius
        return self.offRadius

    def __configureAnimationStage0(self:SoftwareLEDPin, dt:float):
        self.isLit = False

    def __configureAnimationStage1(self:SoftwareLEDPin, dt:float):
        self.isLit = True

    animationStageConfigureDelegates = [__configureAnimationStage0, __configureAnimationStage1]
    animationStageLengthsInMilliseconds = [1000, 2000]
    currentAnimationStage = 0

    def __resetAnimation(self:SoftwareLEDPin):
        self.currentAnimationStage = 0
        self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[0]

    def __updateAnimation(self:SoftwareLEDPin, dt:float):
        self.timeUntilNextAnimationStage -= dt
        if self.timeUntilNextAnimationStage <= 0:
            self.currentAnimationStage += 1
            if self.currentAnimationStage >= len(self.animationStageConfigureDelegates):
                self.currentAnimationStage = 0
            self.timeUntilNextAnimationStage = self.animationStageLengthsInMilliseconds[self.currentAnimationStage]

        self.animationStageConfigureDelegates[self.currentAnimationStage](self, dt)

    def updateTick(self:SoftwareLEDPin, dt:float):
        # if not flashing, ensure anim props are reset
        if not self.isFlashing:
            self.__resetAnimation()
        
        self.__updateAnimation(dt)

    def renderTick(self:SoftwareLEDPin, screen:pygame.Surface):
        pygame.draw.circle(screen, self.__getColour(), self.position, self.__getRadius())
        text = pygame.font.Font('freesansbold.ttf', 12).render(self.label, True, 'white')
        screen.blit(text, pygame.rect.Rect(self.position.x + self.onRadius + 4, self.position.y - self.onRadius/2, 0,0))