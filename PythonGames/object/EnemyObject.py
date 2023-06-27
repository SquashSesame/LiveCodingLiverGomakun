import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.LifeObject import *

# Enemy 共通基底クラス
class EnemyObject(LifeObject):
    # Enemy State
    STATE_START = 0
    STATE_APPEAR = 1
    STATE_NORMAL = 2
    STATE_ATTACK = 3
    
    def __init__(self, name, colsize, centerObj, ofx, ofy, waitTime, stx, sty, life, score):
        super().__init__(name, colsize, stx, sty, life)
        # 速度は下方向に等速移動
        self.center = centerObj
        self.off_x = ofx
        self.off_y = ofy
        self.spdx = 0
        self.spdy = 0
        self.stx = stx
        self.sty = sty
        self.score = score
        # Appear
        self.appearTime = 2.0 # 出現移動時間
        # State
        self.waitTimer = waitTime
        self.state = self.STATE_START

    def updateState(self, deltaTime):
        #===========
        # State
        #===========
        if self.state == self.STATE_START:
            # Start Waiting
            self.waitTimer -= deltaTime
            if self.waitTimer <= 0.0:
                # end of wating
                self.waitTimer = 0
                self.state = self.STATE_APPEAR
        elif self.state == self.STATE_APPEAR:
            # move to offset pos
            self.waitTimer += deltaTime
            if self.waitTimer >= self.appearTime:
                # end of moving
                self.waitTimer = self.appearTime
                self.state = self.STATE_NORMAL
            rate = self.waitTimer/self.appearTime
            self.px = self.interOutQuad( self.stx, (self.center.px + self.off_x), rate)
            self.py = self.interOutQuad( self.sty, (self.center.py + self.off_y), rate)
        elif self.state == self.STATE_NORMAL:        
            # スピード方向に移動
            # self.px += self.spdx * deltaTime
            # self.py += self.spdy * deltaTime
            self.px = self.center.px + self.off_x
            self.py = self.center.py + self.off_y 
    
    def onDead(self):
        if not self.is_dead:
            # Dead Flag ON
            self.is_dead = True
            # Add Score
            g.score.addScore(self.score)
            # Dead to EnemyCenter
            g.enemyCenter.deadEnemy()
            # Dead SE
            g.deadSE.play()
            super().onDead()       

