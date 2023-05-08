import pygame
import sys
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT


pygame.init()
SURFACE = pygame.display.set_mode([800, 600])
s_keymap = []
s_objects = []


class GObject:
    def __init__(self, px, py):
        self.px = px
        self.py = py
        # self.image = pygame.image
        # self.rect = 
    
    def update(self):
        pass

    def draw(self):
        SURFACE.blit(self.image,
            (self.px - self.rect.centerx,
             self.py - self.rect.centery))




class Bullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__(px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.image = pygame.image.load('img/player.png')
        self.rect = self.image.get_rect()
    
    def update(self):
        self.px += self.spdx
        self.py += self.spdy
    



class Player(GObject):
    def __init__(self, px, py):
        super().__init__(px, py)
        self.image = pygame.image.load('img/player.png')
        self.rect = self.image.get_rect()
    
    def update(self):
        global s_keymap
        if K_LEFT in s_keymap:
            self.px -= 2
        if K_RIGHT in s_keymap:
            self.px += 2
        if K_SPACE in s_keymap:
            # タマ出す
            s_objects.append(
                Bullet(self.px,
                       self.py,
                       0, -4))


def main():
    # 初期化
    
    player = Player(400, 300)
    
    # メインループ
    while True:
        
        # ウィンドウメッセージ
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
        
        # プレイヤーの移動
        player.update()

        # オブジェクトの更新
        for obj in s_objects:
            obj.update()

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


