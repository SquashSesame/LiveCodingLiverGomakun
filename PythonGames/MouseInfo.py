import pygame
import sys

import Defines as g

class MouseInfo:
    def __init__(self):
        self.px = 0
        self.py = 0
        self.px_o = 0
        self.py_o = 0
        self.px_delta = 0
        self.py_delta = 0
        self.btn_l = False
        self.btn_r = False
    
    def setPos(self, pos):
        self.px_o = self.px
        self.py_o = self.py
        self.px = pos[0]
        self.py = pos[1]
        self.px_delta = self.px - self.px_o
        self.py_delta = self.py - self.py_o
        

