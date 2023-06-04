import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *
from enemy.EnemyUFO import *
from enemy.Enemy00 import *

class EnemyCenter(GObject):
    STAGE_INFO = -2
    START_POS = -1
    ENE_E = 0
    ENE_U = 1
    MARGIN = 40
    
    def __init__(self, stageTbl, funcEnd):
        self.scrRect = g.SURFACE.get_rect()
        super().__init__("center", 0,
                self.scrRect.centerx, self.scrRect.centery - 100)
        # Enemy generate
        self.stageTbl = stageTbl
        self.stageTitle = ""
        self.startPos = []
        # move
        self.moveAngle = 0
        self.enemyCount = 0
        self.funcEndOfEnemy = funcEnd
        # state Information
        self.setupStateInfo()


    def deadEnemy(self):
        self.enemyCount -= 1
        if self.enemyCount <= 0:
            self.enemyCount = 0
            # callback
            if self.funcEndOfEnemy:
                self.funcEndOfEnemy()


    def setupStateInfo(self):
        for it in self.stageTbl:
            if it[0] == self.STAGE_INFO:
                # state Information
                self.stageTitle = it[1]

        
    def setupEnemy(self):
        waitTimeCount = 0
        for it in self.stageTbl:
            if it[0] == self.START_POS:
                # start postion
                self.startPos.append((it[1], it[2]))
            elif it[0] >= 0:
                # enemy offset
                stPos = self.startPos[it[1]]
                enemy = None
                if it[0] == self.ENE_E:
                    # (centerObj, ofx, ofy, waitTime, stx, sty)
                    enemy = Enemy00( self, it[2], it[3], waitTimeCount, stPos[0], stPos[1])
                elif it[0] == self.ENE_U:
                    # (centerObj, ofx, ofy, waitTime, stx, sty)
                    enemy = EnemyUFO( self, it[2], it[3], waitTimeCount, stPos[0], stPos[1])
                if enemy:
                    g.objects.append(
                        enemy
                    )
                    self.enemyCount += 1
                # wait time
                waitTimeCount += 0.1
            
    def update(self, deltaTime):
        self.moveAngle += deltaTime
        self.px = self.scrRect.centerx + math.cos(self.moveAngle) * 40
        self.py = self.scrRect.centery - 100 + math.sin(self.moveAngle * 5) * 10


