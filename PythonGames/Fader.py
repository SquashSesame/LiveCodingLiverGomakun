import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *

class Fader(GObject):
    def __init__(self):
        super().__init__("fader", 0, 0, 0)
        self.image = None
        self.rect = g.SURFACE.get_rect()
        self.is_fading = False
        self.is_end = False
        self.alpha = 0.0
        self.src_alpha = 0.0
        self.trg_alpha = 0.0
        self.timer = 0
        self.fadeTime = 0.5
        self.img_alpha = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.img_alpha.set_colorkey((0,0,0), pygame.RLEACCEL)
        self.funcEnd = None
    
    def fadeIn(self, fadeTime, funcEnd):
        self.src_alpha = self.alpha
        self.trg_alpha = 0.0
        self.fadeTime = fadeTime
        self.timer = 0
        self.is_fading = True
        self.is_end = False
        self.funcEnd = funcEnd

    def fadeOut(self, fadeTime, funcEnd):
        self.src_alpha = self.alpha
        self.trg_alpha = 255
        self.fadeTime = fadeTime
        self.timer = 0
        self.is_fading = True
        self.is_end = False
        self.funcEnd = funcEnd

    def update(self, deltaTime):
        if self.is_fading:
            # fade Timer
            self.timer += deltaTime
            if self.timer >= self.fadeTime:
                # fade End
                self.timer = self.fadeTime
                self.is_end = True
                self.is_fading = False
                # call func End
                if self.funcEnd:
                    self.funcEnd()
            # fade Alpha
            curTime = self.timer / self.fadeTime
            self.alpha = self.src_alpha + (self.trg_alpha - self.src_alpha) * curTime

    def draw(self):
        self.img_alpha.fill((0,0,0,self.alpha))
        g.SURFACE.blit(self.img_alpha, (0,0))
                
        # pygame.draw.rect(g.SURFACE, 
        #         (0,0,0),
        #         Rect(
        #             400 - self.rect.width * self.alpha * 0.5,
        #             300 - self.rect.height * self.alpha * 0.5,
        #             self.rect.width * self.alpha,
        #             self.rect.height * self.alpha
        #             )
        #         )

