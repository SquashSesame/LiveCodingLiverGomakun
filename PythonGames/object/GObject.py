
import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g

class GObject:
    def __init__(self, name, colsize, px, py):
        self.name = name
        self.col_size = colsize
        self.px = px
        self.py = py
        self.is_dead = False
        self.is_hide = False
        self.scale = 4
        self.cellSize = 8 * self.scale
        self.image = None
        self.rect = None
    
    def update(self, deltaTime):
        pass

    def draw(self):
        if self.image:
            g.SURFACE.blit(self.image,
                (self.px - self.rect.centerx,
                self.py - self.rect.centery))

    def checkWithoutScreen(self):
        scrRect = g.SURFACE.get_rect()
        if self.px < (scrRect.left - self.rect.centerx):
            return True
        if self.px > (scrRect.right + self.rect.centerx):
            return True
        if self.py < (scrRect.top - self.rect.centery):
            return True
        if self.py > (scrRect.bottom + self.rect.centery):
            return True
        return False

    def makeAnimList(self, animPtn):
        animList = []
        for ptn in animPtn:
            animList.append(
                Rect(
                    ptn[0] * self.cellSize,
                    ptn[1] * self.cellSize,
                    self.cellSize,
                    self.cellSize))
        return animList

    # ２つの距離の２乗
    def isHitPlayer(self):
        # 当たり判定をする
        if not g.player.is_dead:
            sx = g.player.px - self.px
            sy = g.player.py - self.py
            distance2 = sx * sx + sy * sy
            checksize  = g.player.col_size + self.col_size
            checksize = checksize * checksize
            if distance2 < checksize:
                return True
        return False

    # 線形補間
    def interLinear(self, st, ed, rate):
        return st + (ed - st) * rate

    # サイン補間 
    def interOutQuad(self, st, ed, rate):
        return st + (ed - st) * math.sin(math.pi * 0.5 * rate)

