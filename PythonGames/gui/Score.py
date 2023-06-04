import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *

class Score(GObject):
    def __init__(self):
        super().__init__("score", 0, 400, 8)
        # Font
        self.textFont = pygame.font.SysFont('MS Gothic', 40)
        self.textScore = self.textFont.render("SCORE", True, (255,255,255))
        self.resetScore()
        self.addScore(0)
        
    def resetScore(self):
        self.totalScore = 0
    
    def addScore(self, score):
        self.totalScore += score
        self.textScoreNum = self.textFont.render(
            f'{self.totalScore:08}', True, (255,255,255))
    
    def update(self, deltaTime):
        pass

    def draw(self):
        scrRect = g.SURFACE.get_rect()
        g.SURFACE.blit(self.textScore,
            ((scrRect.width - self.textScore.get_rect().width) * 0.5, 8))
        g.SURFACE.blit(self.textScoreNum,
            ((scrRect.width - self.textScoreNum.get_rect().width) * 0.5, 48))
