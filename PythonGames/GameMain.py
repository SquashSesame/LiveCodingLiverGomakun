import pygame
import sys
import time
import random
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN


pygame.init()
SURFACE = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Live Coding Liver")
s_keymap = []
s_objects = []
s_imageList = {}


class GObject:
    def __init__(self, name, colsize, px, py):
        self.name = name
        self.col_size = colsize
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

    def onHit(self, attack):
        pass
    
    def onDead(self):
        pass

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
        super().__init__("bullet", 8, px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.attack = 1
        self.image = s_imageList['bullet'] # pygame.image.load('img/bullet.png')
        self.rect = self.image.get_rect()
    
    def update(self, deltaTime):
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面外へ行ったか？
        if self.checkWithoutScreen():
            self.is_dead = True
        # 敵にあたったか？
        hitEnemty = self.getHitEnemy()
        if hitEnemty:
            # 敵にあたった！！
            self.is_dead = True
            hitEnemty.onHit(self.attack)
    
    # あたった敵を取得
    def getHitEnemy(self):
        for obj in s_objects:
            if obj == self:
                continue

            if obj.name == "enemy":
                # 当たり判定をする
                sx = obj.px - self.px
                sy = obj.py - self.py
                distance2 = sx * sx + sy * sy
                checksize  = obj.col_size + self.col_size
                checksize = checksize * checksize
                if distance2 < checksize:
                    return obj
                
        return None




class Player(GObject):
    def __init__(self, px, py):
        super().__init__("player", 16, px, py)
        self.image = s_imageList['player'] #pygame.image.load('img/player.png')
        self.rect = self.image.get_rect()
        self.has_shoted = False
    
    def update(self, deltaTime):
        global s_keymap
        scrRect = SURFACE.get_rect()
        self.speed = 200
        
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
                        0, -400))
        else:
            self.has_shoted = False



class CircleEffect(GObject):
    def __init__(self, px, py):
        super().__init__("effect", 0, px, py)
        self.halfsz = 0
        self.time = 3
        self.end_radius = 100
    
    def update(self, deltaTime):
        self.halfsz += self.end_radius * deltaTime * self.time
        if self.halfsz > self.end_radius:
            self.is_dead = True
    
    def draw(self):
        pygame.draw.circle(
            SURFACE,
            (255,0,0),
            (self.px, self.py),
            self.halfsz,
            1 )


class EnemyUFO(GObject):
    def __init__(self):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "enemy",
            20,
            random.random() * 600 + 100,
            -32,
        )
        # グラフィックはUFO
        self.image = s_imageList['enemyUFO'] #pygame.image.load('img/enemy_64x32_ufo.png')
        self.rect = self.image.get_rect()
        # 速度は下方向に等速移動
        self.spdx = 0
        self.spdy = 100 + random.random() * 100
    
    def update(self, deltaTime):
        # スピード方向に移動
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime

        # 画面の下に消えたら自動削除        
        scrRect = SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
            return True
        
    def onHit(self, attack):
        #TODO: ダメージ計算を入れたい
        self.onDead()
    
    def onDead(self):
        #TODO： やられエフェクトを出して死亡
        self.is_dead = True
        s_objects.append(
            CircleEffect(self.px, self.py)
        )


def main():
    # 初期化
    s_imageList['player'] = pygame.image.load('img/player.png')
    s_imageList['bullet'] = pygame.image.load('img/bullet.png')
    s_imageList['enemyUFO'] = pygame.image.load('img/enemy_64x32_ufo.png')
    
    
    
    player = Player(400, 300)
    preTime = time.perf_counter()
    
    enemyTime = 0
    
    
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
        
        # 敵を出現させる
        enemyTime += deltaTime
        if enemyTime >= 1.0:
            enemyTime = 0
            s_objects.append(
                EnemyUFO()
            )
        
        
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


