
import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *

class LifeGage(GObject):
    def __init__(self):
        super().__init__("lifegage", 0, 32, 32)
        self.image = g.imageList['miscellaneous'] #pygame.image.load('img/player.png')
        self.animList = self.makeAnimList([[0,4]])
        self.imgRect = self.animList[0]
        self.widthHeart = 7 * self.scale

    def draw(self):
        for hp in range(g.player.life):        
            g.SURFACE.blit(
                pygame.transform.scale_by(
                    self.image, self.scale),
                (self.px + hp * self.widthHeart, self.py),
                self.imgRect)
