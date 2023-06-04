import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.EnemyObject import *
from effect.CircleEffect import *

class Enemy00(EnemyObject):
    def __init__(self, centerObj, ofx, ofy, waitTime, stx, sty):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "enemy",
            20,
            centerObj, ofx, ofy, waitTime, stx, sty,
            1,
            10
        )
        # グラフィックはUFO
        self.image = g.imageList['ships']
        self.animList = self.makeAnimList([[5,0]])
        self.rect = self.imgRect = self.animList[0]
    
    def update(self, deltaTime):
        #===========
        # State
        #===========
        self.updateState(deltaTime)

        #===========
        # Common
        #===========
        # Player HIT?
        if self.isHitPlayer():
            g.player.onDamage(1)
        # 画面の下に消えたら自動削除        
        scrRect = g.SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
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
        #TODO: ダメージを受けた表現
        
    
    def onDead(self):
        #TODO： やられエフェクトを出して死亡
        super().onDead()
        g.objects.append(
            CircleEffect(self.px, self.py)
        )

