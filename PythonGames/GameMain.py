import pygame
import sys
import time
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN


pygame.init()
SURFACE = pygame.display.set_mode([800, 600])
s_keymap = []
s_objects = []


class GObject:
    def __init__(self, px, py):
        self.px = px
        self.py = py
        self.is_dead = False
        # self.image = pygame.image
        # self.rect = 
    
    def update(self, deltaTime):
        pass

    def draw(self):
        SURFACE.blit(self.image,
            (self.px - self.rect.centerx,
             self.py - self.rect.centery))

    def checkWithoutScreen(self):
        scrRect = SURFACE.get_rect()
        if self.px < (scrRect.left - self.rect.centerx):
            return True
        
        if self.px > (scrRect.right + self.rect.centerx):
            return True
        
        if self.py < (scrRect.top - self.rect.centery):
            return True
        
        if self.py > (scrRect.bottom + self.rect.centery):
            return True

        return False




class Bullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__(px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.image = pygame.image.load('img/bullet.png')
        self.rect = self.image.get_rect()
    
    def update(self, deltaTime):
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面外へ行ったか？
        if self.checkWithoutScreen():
            self.is_dead = True


class Player(GObject):
    def __init__(self, px, py):
        super().__init__(px, py)
        self.image = pygame.image.load('img/player.png')
        self.rect = self.image.get_rect()
        self.has_shoted = False
    
    def update(self, deltaTime):
        global s_keymap
        scrRect = SURFACE.get_rect()
        self.speed = 100
        
        if K_LEFT in s_keymap:
            self.px -= self.speed * deltaTime
            if self.px < (scrRect.left + self.rect.centerx):
                self.px = scrRect.left + self.rect.centerx
            
        if K_RIGHT in s_keymap:
            self.px += self.speed * deltaTime
            if self.px > (scrRect.right - self.rect.centerx):
                self.px = scrRect.right - self.rect.centerx
            
        if K_UP in s_keymap:
            self.py -= self.speed * deltaTime
            if self.py < (scrRect.top + self.rect.centery):
                self.py = scrRect.top + self.rect.centery
            
        if K_DOWN in s_keymap:
            self.py += self.speed * deltaTime
            if self.py > (scrRect.bottom - self.rect.centery):
                self.py = scrRect.bottom - self.rect.centery
            
        if K_SPACE in s_keymap:
            if not self.has_shoted:
                self.has_shoted = True
                # タマ出す
                s_objects.append(
                    Bullet(self.px, self.py,
                        0, -200))
        else:
            self.has_shoted = False


def main():
    # 初期化
    
    player = Player(400, 300)
    preTime = time.perf_counter()
    
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
            elif event.type == KEYDOWN:
                if not event.key in s_keymap:
                    s_keymap.append(event.key)
            elif event.type == KEYUP:
                s_keymap.remove(event.key)        
        
        ###############
        # 更新
        ###############
        
        # デルタタイム計算
        curTime = time.perf_counter()
        deltaTime = curTime - preTime
        preTime = curTime
        # print("time ", curTime, " delta ", deltaTime)
        
        
        # プレイヤーの移動
        player.update(deltaTime)


        killList = []

        # オブジェクトの更新
        for obj in s_objects:
            if not obj.is_dead:
                obj.update(deltaTime)

            if obj.is_dead:
                killList.append(obj)
            
        # 自動削除
        if len(killList) > 0:
            for obj in killList:
                s_objects.remove(obj)


        ###############
        # 画面描画
        ###############

        SURFACE.fill((255,255,255))
        # プレイヤーの描画
        player.draw()

        # オブジェクトの描画
        for obj in s_objects:
            obj.draw()
        
        # ウィンドウ出す
        pygame.display.update()    


if __name__ == "__main__":
    main()       
    # end main


