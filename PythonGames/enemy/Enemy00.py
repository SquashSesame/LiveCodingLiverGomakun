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

    STATE_ATK_FOWARD = 3    # 前に出る
    STATE_ATK_BULLET = 4    # 弾を出す 
    STATE_ATK_RETURN = 5    # 戻る

    
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
        self.normalTime = 2.0 + random.random() * 5
        self.stateTimer = self.normalTime
    
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

    def updateState(self, deltaTime):
        #===========
        # State
        #===========
        super().updateState(deltaTime)

        if self.state == self.STATE_NORMAL:
            # 一定時間になったら攻撃モードに移行する
            self.stateTimer -= deltaTime
            if self.stateTimer <= 0:
                # 攻撃開始！
                self.state = self.STATE_ATK_FOWARD
                self.aimPy = self.py + 50 + random.random() * 150
                self.stateTimer = 0
                self.stateTime = 2.0
                self.stx = self.px
                self.sty = self.py
        elif self.state == self.STATE_ATK_FOWARD:
            # ランダムな位置まで前進する
            self.stateTimer += deltaTime
            rate = self.stateTimer / self.stateTime
            if rate >= 1.0:
                # FOWARDは終了して、BULLETへ移行する
                rate = 1.0
                self.state = self.STATE_ATK_BULLET
            self.py = self.interOutQuad( self.sty, self.aimPy, rate)
        elif self.state == self.STATE_ATK_BULLET:
            # プレイヤーに向かって弾を出す
            if random.random() > 0.8:
                self.shotBulletToPlayer()
            self.state = self.STATE_ATK_RETURN
        elif self.state == self.STATE_ATK_RETURN:
            # 定位置まで移動したらNORMALステートに戻る
            self.waitTimer = 0
            self.stx = self.px
            self.sty = self.py
            self.state = self.STATE_APPEAR
