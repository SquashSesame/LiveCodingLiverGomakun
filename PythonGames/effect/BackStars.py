import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *


class BackStars(GObject):
    def __init__(self):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "back",
            0,
            random.random() * 600 + 100,
            -32
        )
        self.rect = Rect(0,0,8,8)
        self.color = Color((
            random.random() * 230 + 20,
            random.random() * 230 + 20,
            random.random() * 230 + 20)
        )
        # 速度は下方向に等速移動
        self.spdx = 0
        self.spdy = 100 + random.random() * 400
    
    def update(self, deltaTime):
        # スピード方向に移動
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面の下に消えたら自動削除        
        scrRect = g.SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
            self.is_dead = True
        
    def draw(self):
        pygame.draw.lines(
            g.SURFACE,
            self.color, False, 
            ([self.px, self.py-4],
             [self.px, self.py+4]) )
