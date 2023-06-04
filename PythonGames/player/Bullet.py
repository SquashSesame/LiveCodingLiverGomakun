import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class Bullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__("bullet", 8, px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.attack = 1
        self.image = g.imageList['miscellaneous'] # pygame.image.load('img/bullet.png')
        self.rect = Rect(12*8, 7*8, 8, 8)
        self.scale = 4
        self.animList = self.makeAnimList([[12,7]])
        self.rect = self.imgRect = self.animList[0]
    
    def update(self, deltaTime):
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面外へ行ったか？
        if self.checkWithoutScreen():
            self.is_dead = True
        # 敵にあたったか？
        hitEnemty = self.getHitEnemy()
        if hitEnemty:
            # 敵にあたった！！
            self.is_dead = True
            hitEnemty.onDamage(self.attack)
    
    def draw(self):
        g.SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
            (self.px - self.imgRect.width * 0.5,
             self.py - self.imgRect.height * 0.5),
            self.imgRect)

    
    # あたった敵を取得
    def getHitEnemy(self):
        for obj in g.objects:
            if obj == self:
                continue

            if obj.name == "enemy":
                if not obj.is_dead:
                    # 当たり判定をする
                    sx = obj.px - self.px
                    sy = obj.py - self.py
                    distance2 = sx * sx + sy * sy
                    checksize  = obj.col_size + self.col_size
                    checksize = checksize * checksize
                    if distance2 < checksize:
                        return obj
                
        return None

