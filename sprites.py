import pygame as pg
from pygame.sprite import Sprite

from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')
class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.score = 0
        self.cd = Cooldown()
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        self.cd.ticking()
        # CHECKING FOR COLLISION WITH MOBS HERE>>>>>
        hits = pg.sprite.spritecollide(self, self.game.all_mobs, False)
        if hits:
            print ("i hit a mob")
            # player.hitpoints -= 10
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # self.acc.y += self.vel.y * -0.3
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
       

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
class Boundary(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        # if the boundary is categorized as moving veritcally or horizontally, it will move that way. 
        if self.category == "moving vertically" or "moving horizontally":
            self.speed = 2
    def update(self):
        # If the boundary's category is moving horizontally, it will continue to move between the edges of the screen.
        if self.category == "moving horizontally":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        # if the boundary's category is moving vertically, it will move up and down, hitting the screen each time
        if self.category == "moving vertically":
            self.rect.y += self.speed
            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:
                self.speed = -self.speed

# class jumpPlatform(Sprite):
#     def __init__(self, x, y, w, h, category):
#         Sprite.__init__(self)
#         self.image = pg.Surface((w, h))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.category = category
#         self.speed = 0
#         if self.category == "moving":
#             self.speed = 5
#     def update(self):
#         if self.category == "moving":
#             self.rect.x += self.speed
#             if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
#                 self.speed = -self.speed
class Mob(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving vertically" or "moving horizontally":
            self.speed = 5
    def update(self):
        if self.category == "moving horizontally":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        if self.category == "moving vertically":
            self.rect.y += self.speed
            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:
                self.speed = -self.speed
# class Coin(Sprite):
#     def __init__(self, x, y, w, h, category):
#         Sprite.__init__(self)
#         self.image = pg.image.load(os.path.join(img_folder, 'mario.png')).convert()
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.category = category
#         self.speed = 0
#         if self.category == "moving":
#             self.speed = 5
#     def update(self):
#         if self.category == "moving":
#             self.rect.x += self.speed
#             if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
#                 self.speed = -self.speed   



# class Mob(Sprite):
#     def __init__(self, x, y, w, h, kind):
#         Sprite.__init__(self)
#         self.image = pg.Surface((w, h))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.kind = kind
#         self.pos = vec(WIDTH/2, HEIGHT/2)

class Coin(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'mario.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 5  
        if self.category == "moving":
                self.rect.y += self.speed
                if self.rect.y > HEIGHT/2 or self.rect.y < 0:
                    self.speed = -self.speed
                    self.rect.y += 25

    def update(self):
        pass