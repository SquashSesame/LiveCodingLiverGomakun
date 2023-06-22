import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from scene.Scene import *
from effect.BackStars import *
from Fader import *
# from scene.GameScene import *


class TitleScene(Scene):    
    def __init__(self):
        # オブジェクトの初期化
        g.objects.clear()
        # Font
        self.textFont80 = pygame.font.SysFont('MS Gothic', 80)
        self.textTitle = self.textFont80.render("17Live ATTACK", True, (255,255,255))
        self.textFont40 = pygame.font.SysFont('MS Gothic', 40)
        self.textSTART = self.textFont40.render("PRESS SPACE KEY TO START", True, (255,255,255))
        self.textSndRights = self.textFont40.render("Sound by MaouDamashii", True, (255,255,255))
        self.status = -1
        # Back Stars
        self.timerStar = random.random() * 0.1
        # BGM
        pygame.mixer.music.load(g.soundList['bgm title'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        # fade in
        g.fader.fadeIn(0.5, None)

    def getSceneStatus(self):
        return self.status

    def nextScene(self):
        return g.createGameScene()

    def update(self, deltaTime):
        # back star
        self.timerStar -= deltaTime
        if self.timerStar <= 0.0:
            self.timerStar = random.random() * 0.1
            g.objects.append(
                BackStars()
            )
            g.objects.append(
                BackStars()
            )
        # waiting key
        if K_SPACE in g.keymap or g.mouse.btn_l:
            if not g.fader.is_fading:
                pygame.mixer.music.fadeout(500)
                g.fader.fadeOut(0.5, self.cbFadeEnd)

    def cbFadeEnd(self):
        self.status = 0
        

    def draw(self):
        g.SURFACE.blit(self.textTitle,
            (400 - self.textTitle.get_rect().width * 0.5, 200))

        g.SURFACE.blit(self.textSTART,
            (400 - self.textSTART.get_rect().width * 0.5, 400))
        
        g.SURFACE.blit(self.textSndRights,
            (400 - self.textSndRights.get_rect().width * 0.5, 500))
        

