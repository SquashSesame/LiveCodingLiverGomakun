import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class BoxParticle(GObject):
    def __init__(self, px, py):
        super().__init__("particle", 0, px, py)
        self.image = None
        self.rect = None
        self.timer = 0.5 + random.random() * 0.5
        self.spdx = (random.random() - 0.5) * 200
        self.spdy = (random.random() - 0.5) * 200
        self.width = 5 + random.random() * 30
        self.height = self.width #5 + random.random() * 100

    
    def update(self, deltaTime):
        self.timer -= deltaTime
        if self.timer <= 0:
            self.is_dead = True
        else:
            self.spdx -= self.spdx / 5 * deltaTime
            self.spdy -= self.spdy / 5 * deltaTime
            self.px += self.spdx * deltaTime
            self.py += self.spdy * deltaTime

    def draw(self):
        pygame.draw.rect(
            g.SURFACE, (255,0,0), 
            (self.px, self.py,
             self.width, self.height), 1
        )

class CircleEffect(GObject):
    def __init__(self, px, py):
        super().__init__("effect", 0, px, py)
        self.halfsz = 0
        self.time = 3
        self.end_radius = 100
        # create particle
        for i in range(20):
            g.objects.append(
                BoxParticle(px, py)
            )
    
    def update(self, deltaTime):
        # # update particle
        # for obj in self.particls:
        #     obj.update(deltaTime)
        # impact
        self.halfsz += self.end_radius * deltaTime * self.time
        if self.halfsz > self.end_radius:
            self.is_dead = True            
    
    def draw(self):
        # # update particle
        # for obj in self.particls:
        #     obj.draw()
        # impact
        pygame.draw.circle(
            g.SURFACE,
            (255,0,0),
            (self.px, self.py),
            self.halfsz,
            1 )

