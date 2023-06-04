import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from object.GObject import *

class Scene:
    def getSceneStatus(self):
        # -1 ... シーン実行中
        # 0〜 ... シーン終了
        return -1
    
    def nextScene(self):
        return None
    
    def update(self, deltaTime):
        pass
    
    def draw(self):
        pass


