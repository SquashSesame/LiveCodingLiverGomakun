import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class EnemyBullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__("bullet", 8, px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.attack = 1
        self.image = g.imageList['eBullet']
        self.rect = self.image.get_rect()
    
    def update(self, deltaTime):
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面外へ行ったか？
        if self.checkWithoutScreen():
            # 画面外
            self.is_dead = True
        # Playerにあたったか？
        if self.isHitPlayer():
            # Playerにあたったか？にあたった！！
            self.is_dead = True
            g.player.onDamage(self.attack)

