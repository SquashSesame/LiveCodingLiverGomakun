import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.EnemyObject import *
from effect.CircleEffect import *

class EnemyBonus(LifeObject):

    def __init__(self, stx, sty, spdx, spdy):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "enemy",
            20,
            stx, sty, 1
        )
        # グラフィックはUFO
        self.image = g.imageList['ships']
        self.animList = self.makeAnimList([[4,5]])
        self.rect = self.imgRect = self.animList[0]
        self.appearTimer = 0.5
        self.spdx = spdx
        self.spdy = spdy
    
    def update(self, deltaTime):
        # Player HIT?
        if self.isHitPlayer():
            g.player.onDamage(1)
        
        # Moving
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime

        # 始めの数秒は画面外判定しない
        self.appearTimer -= deltaTime
        if self.appearTimer <= 0:
            self.appearTimer  = 0
            # 画面の端に到達したら消える        
            if self.checkWithoutScreen() == True:
                self.is_dead = True

        
    def draw(self):
        g.SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
            (self.px - self.imgRect.width * 0.5,
             self.py - self.imgRect.height * 0.5),
            self.imgRect)

    def onDamage(self, attack):
        super().onDamage(attack)
    
    def onDead(self):
        #TODO:画面内ならボーナスオブジェクトを出現
        
        # やられエフェクトを出して死亡
        super().onDead()
        g.objects.append(
            CircleEffect(self.px, self.py)
        )
