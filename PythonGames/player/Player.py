import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.LifeObject import *
from player.Bullet import *
from effect.CircleEffect import *

class Player(LifeObject):
    ANIM_RIGHT = 0
    ANIM_MIDDLE = 1
    ANIM_LEFT = 2
    
    def __init__(self, px, py):
        super().__init__("player", 16, px, py, 10)
        self.image = g.imageList['ships'] #pygame.image.load('img/player.png')
        self.rect = Rect(0,0,8,8)
        self.has_shoted = False
        self.speed = 300
        self.animList = self.makeAnimList([[0,0],[1,0],[2,0]])
        self.imgRect = self.animList[self.ANIM_MIDDLE]
        # Muteki 
        self.is_muteki = False
        self.timerMuteki = 0
        self.mutekiBlinkTime = 0.1
        self.timerBlinkTime = 0
        # バーニア
        self.animIndexBaner = 0
        self.animTimerBaner = 0
        self.imgBaner = g.imageList['miscellaneous']
        self.animListBaner = self.makeAnimList([[5,1],[6,1],[7,1],[8,1]])
        self.imgRectBaner = self.animListBaner[0]
        # 自動で弾です
        self.timerAutoShooting = 0
        self.autoShootingTime = 0.2
    
    def update(self, deltaTime):
        if self.is_dead:
            return

        scrRect = g.SURFACE.get_rect()
        
        self.imgRect = self.animList[self.ANIM_MIDDLE]
        
        if g.gameStatus == g.GAMESTATUS_GAME:        
            if abs(g.mouse.px_delta) > 2 or abs(g.mouse.py_delta) > 2:
                self.px = g.mouse.px
                self.py = g.mouse.py

            if K_LEFT in g.keymap or g.mouse.px_delta < -2:
                self.imgRect = self.animList[self.ANIM_LEFT]
                self.px -= self.speed * deltaTime 
                if self.px < (scrRect.left + self.rect.centerx):
                    self.px = scrRect.left + self.rect.centerx
                
            if K_RIGHT in g.keymap or g.mouse.px_delta > 2:
                self.imgRect = self.animList[self.ANIM_RIGHT]
                self.px += self.speed * deltaTime 
                if self.px > (scrRect.right - self.rect.centerx):
                    self.px = scrRect.right - self.rect.centerx
                
            if K_UP in g.keymap or g.mouse.py_delta < -2:
                self.py -= self.speed * deltaTime 
                if self.py < (scrRect.top + self.rect.centery):
                    self.py = scrRect.top + self.rect.centery
                
            if K_DOWN in g.keymap or g.mouse.py_delta > 2:
                self.py += self.speed * deltaTime
                if self.py > (scrRect.bottom - self.rect.centery):
                    self.py = scrRect.bottom - self.rect.centery
                
            # if K_SPACE in g.keymap or g.mouse.btn_l:
            #     if not self.has_shoted:
            #         self.has_shoted = True
            #         # タマ出す
            #         g.objects.append(
            #             Bullet(self.px, self.py,
            #                 0, -400))
            # else:
            #     self.has_shoted = False

            # 自動でたま出す
            self.timerAutoShooting -= deltaTime
            if self.timerAutoShooting < 0.0:
                self.timerAutoShooting = self.autoShootingTime
                # タマ出す
                g.objects.append(
                    Bullet(self.px, self.py, 0, -400)
                )
        
        # バーニア
        self.imgRectBaner = self.animListBaner[self.animIndexBaner]
        self.animTimerBaner += deltaTime
        if self.animTimerBaner > 0.1:
            # animation
            self.animTimerBaner = 0
            self.animIndexBaner += 1
            if self.animIndexBaner >= len(self.animListBaner):
                self.animIndexBaner = 0
        
        # 無敵時間
        if self.is_muteki:
            # Blink
            self.timerBlinkTime -= deltaTime
            if self.timerBlinkTime <= 0:
                self.timerBlinkTime = self.mutekiBlinkTime
                self.is_hide = self.is_hide == False
            # Muteki Time 
            self.timerMuteki += deltaTime
            if self.timerMuteki > 1.0:
                self.timerMuteki = 0
                self.is_muteki = False
                self.is_hide = False


    def draw(self):
        if self.is_dead or self.is_hide:
            return
        
        g.SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
                (self.px - self.imgRect.width * 0.5,
                self.py - self.imgRect.height * 0.5),
                self.imgRect
        )
        g.SURFACE.blit(
            pygame.transform.scale_by(
                self.imgBaner, self.scale),
                (self.px - self.imgRectBaner.width * 0.5,
                self.py - self.imgRectBaner.height * 0.5 + 8 * self.scale),
                self.imgRectBaner
        )
        
    def onDamage(self, attack):
        if not self.is_muteki:
            self.is_muteki = True
            super().onDamage(attack)
            # 減った体力を表示に反映
            g.objects.append(
                CircleEffect(self.px, self.py)
            )

    def onDead(self):
        self.is_dead = True
        g.objects.append(
            CircleEffect(self.px, self.py)
        )
        g.gameStatus = g.GAMESTATUS_GAMEOVER
