import pygame
import sys
import time
import random
import math

from pygame.locals import *
import Defines as g
from MouseInfo import *
from object.GObject import *
from object.LifeObject import *
from player.Bullet import *
from enemy.EnemyBullet import *
from Fader import *
from enemy.EnemyCenter import *
from scene.TitleScene import *
from scene.GameScene import *
from scene.EndingScene import *
        
        
# メイン        
def main():
    # global initialize    
    pygame.init()
    pygame.display.set_caption("Live Coding Liver")
    g.SURFACE = pygame.display.set_mode([800, 600])

    g.keymap = []
    g.objects = []
    g.imageList = {}
    g.soundList = {}
    
    # image List
    g.imageList['ships'] = pygame.image.load('img/assets/SpaceShooterAssetPack_Ships.png')
    g.imageList['miscellaneous'] = pygame.image.load('img/assets/SpaceShooterAssetPack_Miscellaneous.png')
    g.imageList['eBullet'] = pygame.image.load('img/e_bullet.png')

    # sound List
    g.soundList['bgm title'] = 'sound/maou_bgm_8bit26.mp3'
    g.soundList['bgm game'] = 'sound/maou_bgm_8bit08.mp3'
    g.soundList['bgm clear'] = 'sound/maou_bgm_8bit13.mp3'
    g.soundList['se shot'] = 'sound/maou_se_system43.mp3'
    g.soundList['se expl'] = 'sound/maou_se_battle_gun05.mp3'
    g.soundList['jg clear'] = 'sound/maou_game_jingle03.mp3'
    g.soundList['jg over'] = 'sound/maou_game_jingle07.mp3'
    
    # global 変数

    g.player = None
    g.score = None
    g.limitTimer = None
    g.enemyCenter = None

    g.LIMIT_TIME = 60
    g.GAMESTATUS_GAME = 0
    g.GAMESTATUS_GAMEOVER = 1
    g.GAMESTATUS_GAMECLEAR = 2
    g.gameStatus = g.GAMESTATUS_GAME

    g.mouse = MouseInfo()
    g.fader = Fader()

    g.createTitleScene = lambda : TitleScene()
    g.createGameScene = lambda : GameScene()
    g.createEndingScene = lambda : EndingScene()

    # ステージバランス
    g.enemyAtkCounter = 0       # ステージ内で攻撃する敵の数
    g.enemyAtkMaxCounter = 1    # ステージ内で攻撃する敵の最大数

    # SE
    g.deadSE = pygame.mixer.Sound(g.soundList['se expl'])
    
    
    pygame.mixer.init()

    # calc for deltaTime
    preTime = time.perf_counter()
    
    
    # Current Scene    
    curScene = g.createTitleScene()
        
    ###################
    # メインループ
    ###################
    while True:

        ###############
        # ウィンドウイベント
        ###############
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Keyboard
            elif event.type == KEYDOWN:
                if not event.key in g.keymap:
                    g.keymap.append(event.key)
            elif event.type == KEYUP:
                g.keymap.remove(event.key)    
            # mouse
            elif event.type == MOUSEMOTION:
                g.mouse.setPos(event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                g.mouse.setPos(event.pos)
                g.mouse.btn_l = True
            elif event.type == MOUSEBUTTONUP:
                g.mouse.setPos(event.pos)
                g.mouse.btn_l = False
        
        ###############
        # 更新
        ###############
        
        # デルタタイム計算
        curTime = time.perf_counter()
        deltaTime = curTime - preTime
        preTime = curTime
        
        # Scene update
        curScene.update(deltaTime)
        
        # Fader update
        g.fader.update(deltaTime)
        
        killList = []

        # オブジェクトの更新
        for obj in g.objects:
            if not obj.is_dead:
                obj.update(deltaTime)

            if obj.is_dead:
                killList.append(obj)
            
        # 自動削除
        if len(killList) > 0:
            for obj in killList:
                g.objects.remove(obj)


        ###############
        # 画面描画
        ###############

        g.SURFACE.fill((0, 0, 0))

        # オブジェクトの描画
        for obj in g.objects:
            obj.draw()
        
        # Scene draw
        curScene.draw()
        
        # Fader draw
        g.fader.draw()
        
        # Switch Scne
        if curScene.getSceneStatus() >= 0:
            curScene = curScene.nextScene()
        
        # ウィンドウ出す
        pygame.display.update()    


if __name__ == "__main__":
    main()       
    # end main


