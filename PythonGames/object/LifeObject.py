
import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class LifeObject(GObject):
    def __init__(self, name, colsize, px, py, life):
        super().__init__(name, colsize, px, py)
        self.life = life
    
    def onDamage(self, attack):
        self.life -= attack
        if self.life <= 0:
            self.onDead()
    
    def onDead(self):
        self.is_dead = True
    
