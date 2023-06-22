import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from scene.Scene import *
from player.Player import *
from gui.LifeGage import *
from gui.Score import *
from gui.LimitTimer import *
from enemy.EnemyCenter import *
from stage.StageAll_Tbl import *
from effect.BackStars import *

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
# from scene.TitleScene import *
# from scene.EndingScene import *

class GameScene(Scene):
    STATE_TITLE = 0
    STATE_GAME = 1
    STATE_CLEAR = 2
    STATE_GAMECLEAR = 3
    STATE_NEXTSCENE = -1
    
    def __init__(self):
        # オブジェクトの初期化
        g.objects.clear()
        # プレイヤーオブジェクトの生成
        scrRect = g.SURFACE.get_rect()
        g.player = Player(scrRect.centerx, scrRect.bottom - 100)
        g.lifeGage = LifeGage()
        g.score = Score()
        g.limitTimer = LimitTimer(g.LIMIT_TIME, self.cbTimeUp)
        # Font
        self.textFont = pygame.font.SysFont('MS Gothic', 80)
        self.textGAMEOVER = self.textFont.render("GAME OVER", True, (255,0,0))
        self.textSTAGECLEAR = self.textFont.render("STAGE CLEAR", True, (255,0,255))
        # 敵を出現させるタイマー
        self.enemyTime = random.random() + 0.5
        self.status = -1
        # Back Stars
        self.timerStar = random.random() * 0.1
        # BGM
        pygame.mixer.music.load(g.soundList['bgm game'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        # fade in
        g.fader.fadeIn(0.5, None)        
        # init stage
        self.stageNo = 0
        self.initStage(self.stageNo)
        
    # ステージの初期化をする        
    def initStage(self, stageNo):
        # Reset State Timer
        g.limitTimer.reset()
        # Game State
        g.gameStatus = g.GAMESTATUS_GAME
        # State State
        self.state = self.STATE_TITLE
        self.titleTimer = 2.0
        # Enemy Center
        g.enemyCenter = EnemyCenter(StageAll_Tbl[stageNo], self.cbEnemyEmpty)
        # State Title
        self.textSTATETITLE = self.textFont.render(
                g.enemyCenter.stageTitle, True, (255,0,0))
                
    def cbEnemyEmpty(self):
        # 敵全滅
        # Stage Clear
        self.state = self.STATE_CLEAR
        self.titleTimer = 2.0
        g.limitTimer.stop()
    
    def getSceneStatus(self):
        return self.status

    def nextScene(self):
        if g.gameStatus == g.GAMESTATUS_GAME:
            return g.createEndingScene()
        else:
            return g.createTitleScene()

    def update(self, deltaTime):
        #============
        # STATE
        #============
        if self.state == self.STATE_TITLE:
            # show titile
            self.titleTimer -= deltaTime
            if self.titleTimer <= 0:
                self.titleTimer = 0
                # enemy setup
                g.limitTimer.start()
                g.enemyCenter.setupEnemy()
                self.state = self.STATE_GAME
        elif self.state == self.STATE_GAME:
            # game main
            # enemy cente
            g.enemyCenter.update(deltaTime)
        elif self.state == self.STATE_CLEAR:
            # stage clear
            self.titleTimer -= deltaTime
            if self.titleTimer <= 0:
                self.titleTimer = 0
                # next stage
                self.stageNo += 1
                if len(StageAll_Tbl) > self.stageNo:
                    # next stage
                    self.initStage(self.stageNo)
                else:
                    # all stage clear!!
                    self.state = self.STATE_GAMECLEAR
                    g.gameStatus = g.GAMESTATUS_GAME
                    self.titleTimer = 2.0
                    self.textSTAGECLEAR = self.textFont.render(
                        "GAME CLEAR !!", True, (255,0,0))
                    
        elif self.state == self.STATE_GAMECLEAR:
            # GAME CLEAR
            self.titleTimer -= deltaTime
            if self.titleTimer <= 0:
                self.titleTimer = 0
                # fade out
                pygame.mixer.music.fadeout(500)
                g.fader.fadeOut(0.5, self.cbFadeEnd)
                self.state = self.STATE_NEXTSCENE

        elif self.state == self.STATE_NEXTSCENE:
            pass
            
            
        #============
        # Common
        #============
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
        # SCORE
        g.score.update(deltaTime)
        g.limitTimer.update(deltaTime)
        # プレイヤーの移動
        g.player.update(deltaTime)
        g.lifeGage.update(deltaTime)
        # ゲームオーバー
        if g.gameStatus == g.GAMESTATUS_GAMEOVER:
            if K_SPACE in g.keymap:
                # end of game scene
                # fade out
                pygame.mixer.music.fadeout(500)
                g.fader.fadeOut(0.5, self.cbFadeEnd)
                
    def cbTimeUp(self):
        g.gameStatus = g.GAMESTATUS_GAMEOVER
        
    def cbFadeEnd(self):
        self.status = 0

    def draw(self):
            
        # プレイヤーの描画
        g.player.draw()
        g.lifeGage.draw()
        # SCORE
        g.score.draw()
        g.limitTimer.draw()
        
        if self.state == self.STATE_TITLE:
            # STATE TITLE
            g.SURFACE.blit(self.textSTATETITLE,
                (400 - self.textSTATETITLE.get_rect().width * 0.5, 200))
        # STAGE CLEAR?
        if self.state == self.STATE_CLEAR or self.state == self.STATE_GAMECLEAR:
            g.SURFACE.blit(self.textSTAGECLEAR,
                (400 - self.textSTAGECLEAR.get_rect().width * 0.5, 200))        
        # GAME OVER?
        elif g.gameStatus == g.GAMESTATUS_GAMEOVER:
            g.SURFACE.blit(self.textGAMEOVER,
                (400 - self.textGAMEOVER.get_rect().width * 0.5, 200))
