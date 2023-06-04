
import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class LimitTimer(GObject):
    def __init__(self, time, funcEnd):
        super().__init__("timer", 0, 400, 8)
        # Font
        self.textFont = pygame.font.SysFont('MS Gothic', 40)
        self.textTime = self.textFont.render("TIME", True, (255,255,255))
        self.is_start = False
        self.funcEndOfTimer = funcEnd
        self.resetTime = time
        self.reset()
        
    def reset(self):
        self.limitTimer = self.resetTime
    
    def start(self):
        self.is_start = True
    
    def stop(self):
        self.is_start = False

    def isTimeUp(self):
        return self.limitTimer <= 0
    
    def update(self, deltaTime):
        if self.is_start:
            self.limitTimer -= deltaTime
            if self.limitTimer <= 0.0:
                self.limitTimer = 0
                self.is_start = False
                # call back
                if self.funcEndOfTimer:
                    self.funcEndOfTimer()

    def draw(self):
        scrRect = g.SURFACE.get_rect()
        
        self.textTimeNum = self.textFont.render(
            str(int(self.limitTimer)), True, (255,255,255))
        
        g.SURFACE.blit(self.textTime,
            ((scrRect.width - self.textTime.get_rect().width) * 0.5 + 200, 8))
        g.SURFACE.blit(self.textTimeNum,
            ((scrRect.width - self.textTimeNum.get_rect().width) * 0.5 + 200, 48))

