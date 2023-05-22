import pygame
import sys
import time
import random
import math
from pygame.locals import *


pygame.init()
SURFACE = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Live Coding Liver")
s_keymap = []
s_objects = []
s_imageList = {}
s_player = None
s_fader = None

GAMESTATUS_GAME = 0
GAMESTATUS_GAMEOVER = 1
s_gameStatus = GAMESTATUS_GAME


class GObject:
    def __init__(self, name, colsize, px, py):
        self.name = name
        self.col_size = colsize
        self.px = px
        self.py = py
        self.is_dead = False
        self.scale = 4
        self.cellSize = 8 * self.scale
        self.image = None
        self.rect = None
    
    def update(self, deltaTime):
        pass

    def draw(self):
        if self.image:
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

    def makeAnimList(self, animPtn):
        animList = []
        for ptn in animPtn:
            animList.append(
                Rect(
                    ptn[0] * self.cellSize,
                    ptn[1] * self.cellSize,
                    self.cellSize,
                    self.cellSize))
        return animList

    # ２つの距離の２乗
    def isHitPlayer(self):
        # 当たり判定をする
        global s_player
        if not s_player.is_dead:
            sx = s_player.px - self.px
            sy = s_player.py - self.py
            distance2 = sx * sx + sy * sy
            checksize  = s_player.col_size + self.col_size
            checksize = checksize * checksize
            if distance2 < checksize:
                return True
        return False


class LifeObject(GObject):
    def __init__(self, name, colsize, px, py, life):
        super().__init__(name, colsize, px, py)
        self.life = life
    
    def onDamage(self, attack):
        self.life -= attack
        if self.life <= 0:
            self.onDead()
    
    def onDead(self):
        pass

    
class Bullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__("bullet", 8, px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.attack = 1
        self.image = s_imageList['miscellaneous'] # pygame.image.load('img/bullet.png')
        self.rect = Rect(12*8, 7*8, 8, 8)
        self.scale = 4
        self.animList = self.makeAnimList([[12,7]])
        self.rect = self.imgRect = self.animList[0]
    
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
            hitEnemty.onDamage(self.attack)
    
    def draw(self):
        SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
            (self.px - self.imgRect.width * 0.5,
             self.py - self.imgRect.height * 0.5),
            self.imgRect)

    
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


class EnemyBullet(GObject):
    def __init__(self, px, py, spdx, spdy):
        super().__init__("bullet", 8, px, py)
        self.spdx = spdx
        self.spdy = spdy
        self.attack = 1
        self.image = s_imageList['eBullet']
        self.rect = self.image.get_rect()
    
    def update(self, deltaTime):
        global s_player
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面外へ行ったか？
        if self.checkWithoutScreen():
            self.is_dead = True
        # Playerにあたったか？
        if self.isHitPlayer():
            # Playerにあたったか？にあたった！！
            self.is_dead = True
            s_player.onDamage(self.attack)
    

class Player(LifeObject):
    ANIM_RIGHT = 0
    ANIM_MIDDLE = 1
    ANIM_LEFT = 2
    
    def __init__(self, px, py):
        super().__init__("player", 16, px, py, 10)
        self.image = s_imageList['ships'] #pygame.image.load('img/player.png')
        self.rect = Rect(0,0,8,8)
        self.has_shoted = False
        self.is_muteki = False
        self.timerMuteki = 0
        self.speed = 100
        self.animList = self.makeAnimList([[0,0],[1,0],[2,0]])
        self.imgRect = self.animList[self.ANIM_MIDDLE]
        # バーニア
        self.animIndexBaner = 0
        self.animTimerBaner = 0
        self.imgBaner = s_imageList['miscellaneous']
        self.animListBaner = self.makeAnimList([[5,1],[6,1],[7,1],[8,1]])
        self.imgRectBaner = self.animListBaner[0]
    
    def update(self, deltaTime):
        if self.is_dead:
            return

        global s_keymap
        scrRect = SURFACE.get_rect()
        
        self.imgRect = self.animList[self.ANIM_MIDDLE]
        if K_LEFT in s_keymap:
            self.imgRect = self.animList[self.ANIM_LEFT]
            self.px -= self.speed * deltaTime
            if self.px < (scrRect.left + self.rect.centerx):
                self.px = scrRect.left + self.rect.centerx
            
        if K_RIGHT in s_keymap:
            self.imgRect = self.animList[self.ANIM_RIGHT]
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
            self.timerMuteki += deltaTime
            if self.timerMuteki > 1.0:
                self.timerMuteki = 0
                self.is_muteki = False


    def draw(self):
        if self.is_dead:
            return
        
        SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
                (self.px - self.imgRect.width * 0.5,
                self.py - self.imgRect.height * 0.5),
                self.imgRect
        )
        SURFACE.blit(
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
            s_objects.append(
                CircleEffect(self.px, self.py)
            )

    def onDead(self):
        global s_gameStatus
        self.is_dead = True
        s_objects.append(
            CircleEffect(self.px, self.py)
        )
        s_gameStatus = GAMESTATUS_GAMEOVER
        

class LifeGage(GObject):
    def __init__(self):
        super().__init__("lifegage", 0, 32, 32)
        self.image = s_imageList['miscellaneous'] #pygame.image.load('img/player.png')
        self.animList = self.makeAnimList([[0,4]])
        self.imgRect = self.animList[0]

    def draw(self):
        for hp in range(s_player.life):        
            SURFACE.blit(
                pygame.transform.scale_by(
                    self.image, self.scale),
                (self.px + hp * self.cellSize, self.py),
                self.imgRect)


class BoxParticle(GObject):
    def __init__(self, px, py):
        super().__init__("particle", 0, px, py)
        self.image = None
        self.rect = None
        self.timer = 0.5 + random.random() * 0.5
        self.spdx = (random.random() - 0.5) * 200
        self.spdy = (random.random() - 0.5) * 200
        self.width = 5 + random.random() * 30
        self.height = self.width #5 + random.random() * 100

    
    def update(self, deltaTime):
        self.timer -= deltaTime
        if self.timer <= 0:
            self.is_dead = True
        else:
            self.spdx -= self.spdx / 5 * deltaTime
            self.spdy -= self.spdy / 5 * deltaTime
            self.px += self.spdx * deltaTime
            self.py += self.spdy * deltaTime

    def draw(self):
        pygame.draw.rect(
            SURFACE, (255,0,0), 
            (self.px, self.py,
             self.width, self.height), 1
        )


class CircleEffect(GObject):
    def __init__(self, px, py):
        super().__init__("effect", 0, px, py)
        self.halfsz = 0
        self.time = 3
        self.end_radius = 100
        # create particle
        for i in range(20):
            s_objects.append(
                BoxParticle(px, py)
            )
    
    def update(self, deltaTime):
        # # update particle
        # for obj in self.particls:
        #     obj.update(deltaTime)
        # impact
        self.halfsz += self.end_radius * deltaTime * self.time
        if self.halfsz > self.end_radius:
            self.is_dead = True            
    
    def draw(self):
        # # update particle
        # for obj in self.particls:
        #     obj.draw()
        # impact
        pygame.draw.circle(
            SURFACE,
            (255,0,0),
            (self.px, self.py),
            self.halfsz,
            1 )


class EnemyUFO(LifeObject):
    def __init__(self):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "enemy",
            20,
            random.random() * 600 + 100,
            -32,
            3
        )
        # グラフィックはUFO
        self.image = s_imageList['ships']
        self.animList = self.makeAnimList([[9,0]])
        self.rect = self.imgRect = self.animList[0]
        # 速度は下方向に等速移動
        self.spdx = 0
        self.spdy = 100 + random.random() * 1
        # bullet timer
        self.bulletTimer = 1.0 + random.random() * 5
        self.bulletSpeed = 200
    
    def update(self, deltaTime):
        # スピード方向に移動
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        
        # Bullet Timer
        self.bulletTimer -= deltaTime
        if self.bulletTimer <= 0.0:
            self.bulletTimer = 1.0 + random.random() * 5
            if self.py < s_player.py:
                self.shotBulletToPlayer()
        # Player HIT?
        if self.isHitPlayer():
            s_player.onDamage(1)

        # 画面の下に消えたら自動削除        
        scrRect = SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
            self.is_dead = True
        
    def draw(self):
        SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
            (self.px - self.imgRect.width * 0.5,
             self.py - self.imgRect.height * 0.5),
            self.imgRect)
        
    def onDamage(self, attack):
        super().onDamage(attack)
        #TODO: ダメージを受けた表現
        
    def onDead(self):
        #TODO： やられエフェクトを出して死亡
        self.is_dead = True
        s_objects.append(
            CircleEffect(self.px, self.py)
        )

    def shotBulletToPlayer(self):
        # Calc Speed
        global s_player
        spdx = s_player.px - self.px
        spdy = s_player.py - self.py
        length = math.sqrt( spdx * spdx + spdy * spdy)
        spdx = spdx/length * self.bulletSpeed
        spdy = spdy/length * self.bulletSpeed
        # Shot Enemy Bulet
        s_objects.append(
            EnemyBullet(
                self.px, self.py,
                spdx, spdy
            )
        )


class Enemy00(LifeObject):
    def __init__(self):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "enemy",
            20,
            random.random() * 600 + 100,
            -32,
            1
        )
        # グラフィックはUFO
        self.image = s_imageList['ships']
        self.animList = self.makeAnimList([[4,0]])
        self.rect = self.imgRect = self.animList[0]
        # 速度は下方向に等速移動
        self.spdx = 0
        self.spdy = 150 + random.random() * 200
    
    def update(self, deltaTime):
        # スピード方向に移動
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # Player HIT?
        if self.isHitPlayer():
            s_player.onDamage(1)
        # 画面の下に消えたら自動削除        
        scrRect = SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
            self.is_dead = True
        
    def draw(self):
        SURFACE.blit(
            pygame.transform.scale_by(
                self.image, self.scale),
            (self.px - self.imgRect.width * 0.5,
             self.py - self.imgRect.height * 0.5),
            self.imgRect)

    def onDamage(self, attack):
        super().onDamage(attack)
        #TODO: ダメージを受けた表現
        
    
    def onDead(self):
        #TODO： やられエフェクトを出して死亡
        self.is_dead = True
        s_objects.append(
            CircleEffect(self.px, self.py)
        )


class BackStars(GObject):
    def __init__(self):
        # 水平方向にランダムな位置に出現
        super().__init__(
            "back",
            0,
            random.random() * 600 + 100,
            -32
        )
        self.rect = Rect(0,0,8,8)
        self.color = Color((
            random.random() * 230 + 20,
            random.random() * 230 + 20,
            random.random() * 230 + 20)
        )
        # 速度は下方向に等速移動
        self.spdx = 0
        self.spdy = 100 + random.random() * 400
    
    def update(self, deltaTime):
        # スピード方向に移動
        self.px += self.spdx * deltaTime
        self.py += self.spdy * deltaTime
        # 画面の下に消えたら自動削除        
        scrRect = SURFACE.get_rect()
        if self.py > (scrRect.bottom + self.rect.centery):
            self.is_dead = True
        
    def draw(self):
        pygame.draw.lines(
            SURFACE,
            self.color, False, 
            ([self.px, self.py-4],
             [self.px, self.py+4]) )


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

class GameScene(Scene):
    def __init__(self):
        global s_imageList, s_player, s_lifeGage, s_objects, s_gameStatus, s_fader
        # オブジェクトの初期化
        s_objects.clear()
        s_gameStatus = GAMESTATUS_GAME
        # プレイヤーオブジェクトの生成
        s_player = Player(400, 300)
        s_lifeGage = LifeGage()
        # Font
        self.textFont = pygame.font.SysFont('MS Gothic', 80)
        self.textGAMEOVER = self.textFont.render("GAME OVER", True, (255,0,0))
        # 敵を出現させるタイマー
        self.enemyTime = random.random() + 0.5
        self.status = -1
        # Back Stars
        self.timerStar = random.random() * 0.1
        # fade in
        s_fader.fadeIn(0.5, None)
        
    # def cbFuncNon(self):
    #     print("pass")
        
    def getSceneStatus(self):
        return self.status

    def nextScene(self):
        return TitleScene()

    def update(self, deltaTime):
        # 敵を出現させる
        #TODO：将来的には出現テーブルで対応
        self.enemyTime -= deltaTime
        if self.enemyTime <= 0.0:
            self.enemyTime = random.random() + 0.5
            s_objects.append(
                EnemyUFO()
            )
            s_objects.append(
                Enemy00()
            )
            s_objects.append(
                Enemy00()
            )
            s_objects.append(
                Enemy00()
            )
        # back star
        self.timerStar -= deltaTime
        if self.timerStar <= 0.0:
            self.timerStar = random.random() * 0.1
            s_objects.append(
                BackStars()
            )
            s_objects.append(
                BackStars()
            )
        # プレイヤーの移動
        s_player.update(deltaTime)
        s_lifeGage.update(deltaTime)
        # ゲームオーバー
        if s_gameStatus == GAMESTATUS_GAMEOVER:
            if K_SPACE in s_keymap:
                # end of game scene
                # fade out
                s_fader.fadeOut(0.5, self.cbFadeEnd)
                
    def cbFadeEnd(self):
        self.status = 0

    def draw(self):
        # プレイヤーの描画
        s_player.draw()
        s_lifeGage.draw()
        
        # GAGAME OVER?
        if s_gameStatus == GAMESTATUS_GAMEOVER:
            SURFACE.blit(self.textGAMEOVER,
                (400 - self.textGAMEOVER.get_rect().width * 0.5, 200))
        

class TitleScene(Scene):
    def __init__(self):
        global s_imageList, s_player, s_lifeGage, s_objects, s_fader
        # オブジェクトの初期化
        s_objects.clear()
        # Font
        self.textFont80 = pygame.font.SysFont('MS Gothic', 80)
        self.textTitle = self.textFont80.render("17Live ATTACK", True, (255,255,255))
        self.textFont40 = pygame.font.SysFont('MS Gothic', 40)
        self.textSTART = self.textFont40.render("PRESS SPACE KEY TO START", True, (255,255,255))
        self.status = -1
        # Back Stars
        self.timerStar = random.random() * 0.1
        # fade in
        s_fader.fadeIn(0.5, None)

    # def cbFuncNon(self):
    #     print("pass")

    def getSceneStatus(self):
        return self.status

    def nextScene(self):
        return GameScene()

    def update(self, deltaTime):
        # back star
        self.timerStar -= deltaTime
        if self.timerStar <= 0.0:
            self.timerStar = random.random() * 0.1
            s_objects.append(
                BackStars()
            )
            s_objects.append(
                BackStars()
            )
        # waiting key
        if K_SPACE in s_keymap:
            if not s_fader.is_fading:
                s_fader.fadeOut(0.5, self.cbFadeEnd)

    def cbFadeEnd(self):
        self.status = 0
        

    def draw(self):
        SURFACE.blit(self.textTitle,
            (400 - self.textTitle.get_rect().width * 0.5, 200))

        SURFACE.blit(self.textSTART,
            (400 - self.textSTART.get_rect().width * 0.5, 400))


class Fader(GObject):
    def __init__(self):
        super().__init__("fader", 0, 0, 0)
        self.image = None
        self.rect = SURFACE.get_rect()
        self.is_fading = False
        self.is_end = False
        self.alpha = 0.0
        self.src_alpha = 0.0
        self.trg_alpha = 0.0
        self.timer = 0
        self.fadeTime = 0.5
        self.img_alpha = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # colorKey = self.img_alpha.get_at((0,0))
        self.img_alpha.set_colorkey((0,0,0), pygame.RLEACCEL)
        # self.img_alpha.fill((0,0,0), self.img_alpha.get_rect())
        self.funcEnd = None
    
    def fadeIn(self, fadeTime, funcEnd):
        self.src_alpha = self.alpha
        self.trg_alpha = 0.0
        self.fadeTime = fadeTime
        self.timer = 0
        self.is_fading = True
        self.is_end = False
        self.funcEnd = funcEnd

    def fadeOut(self, fadeTime, funcEnd):
        self.src_alpha = self.alpha
        self.trg_alpha = 255
        self.fadeTime = fadeTime
        self.timer = 0
        self.is_fading = True
        self.is_end = False
        self.funcEnd = funcEnd

    def update(self, deltaTime):
        if self.is_fading:
            # fade Timer
            self.timer += deltaTime
            if self.timer >= self.fadeTime:
                # fade End
                self.timer = self.fadeTime
                self.is_end = True
                self.is_fading = False
                # call func End
                if self.funcEnd:
                    self.funcEnd()
            # fade Alpha
            curTime = self.timer / self.fadeTime
            self.alpha = self.src_alpha + (self.trg_alpha - self.src_alpha) * curTime

    def draw(self):
        self.img_alpha.fill((0,0,0,self.alpha))
        # self.img_alpha.fill(
        #     (255,0,0,self.alpha), self.rect, special_flags=pygame.BLEND_RGBA_MULT)
        # self.img_alpha.set_alpha(self.alpha)s
        SURFACE.blit(self.img_alpha, (0,0))
        # pygame.draw.rect(self.img_alpha, (0,0,0,self.alpha), self.img_alpha.get_rect())
                
        # pygame.draw.rect(SURFACE, 
        #         (0,0,0),
        #         Rect(
        #             400 - self.rect.width * self.alpha * 0.5,
        #             300 - self.rect.height * self.alpha * 0.5,
        #             self.rect.width * self.alpha,
        #             self.rect.height * self.alpha
        #             )
        #         )


def main():
    
    global s_player, s_fader
    
    s_imageList['ships'] = pygame.image.load('img/assets/SpaceShooterAssetPack_Ships.png')
    s_imageList['miscellaneous'] = pygame.image.load('img/assets/SpaceShooterAssetPack_Miscellaneous.png')
    s_imageList['enemyUFO'] = pygame.image.load('img/enemy_64x32_ufo.png')
    s_imageList['enemy00'] = pygame.image.load('img/enemy00.png')
    s_imageList['eBullet'] = pygame.image.load('img/e_bullet.png')

    # Fader
    s_fader = Fader()

    # calc for deltaTime
    preTime = time.perf_counter()
        
    curScene = TitleScene()
        
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
        
        # Scene update
        curScene.update(deltaTime)
        
        # Fader update
        s_fader.update(deltaTime)

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

        SURFACE.fill((0, 0, 0))

        # オブジェクトの描画
        for obj in s_objects:
            obj.draw()
        
        # Scene draw
        curScene.draw()
        
        # Fader draw
        s_fader.draw()
        
        # Switch Scne
        if curScene.getSceneStatus() >= 0:
            curScene = curScene.nextScene()
        
        # ウィンドウ出す
        pygame.display.update()    


if __name__ == "__main__":
    main()       
    # end main


