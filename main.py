# This file was created by: Roan Kher
# content from kids can code: http://kidscancode.org/blog/


'''
Goals: Get the coin at the top of the level
Rules: Jump, move in the air, and don't fall to the bottom of the map
Feedback: A level progression at the top of the window
Freedom: Run side to side, jump, drop

Feature Goals: 
Have certain platforms boost me when I double jump on them
Have mobs that will hurt me if I touch them
Add stars that I can get if I reach certain points. 

'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite

import random
from random import randint
import os
from settings import *
from sprites import *
import math
from math import floor
import time


vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # create a group for all sprites
        self.score = 10
        self.coins = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # self.all_jumpPlatforms = pg.sprite.Group()
        self.all_Coins = pg.sprite.Group()
        self.all_Boundaries = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        
        # for j in JUMPPLATFORM_LIST:
        #     jump = jumpPlatform(*j)
        #     self.all_sprites.add(jump)
        #     self.all_jumpPlatforms.add(jump)

        # taking the mobs from the Mob List in settings.py and putting them in the game
        for m in MOB_LIST:
            mobs = Mob(*m)
            self.all_sprites.add(mobs)
            self.all_mobs.add(mobs)
        # taking the coins from the Coins List in settings.py and putting them in the game
        for c in COIN_LIST: 
            coin = Coin(*c)
            self.all_sprites.add(coin)
            self.all_Coins.add(coin)
        # taking the Boundary from the Boundary List in settings.py and putting them in the game
        for bound in BOUND_LIST:
            boundaries = Boundary(*bound)
            self.all_sprites.add(boundaries)
            self.all_Boundaries.add(boundaries)


        # for m in range(0,10):
        #     m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
        #     self.all_sprites.add(m)
        #     self.all_mobs.add(m)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # Given to me by Sean Daly: When the character's x position goes off the side of the screen, it appears on the other side of the screen. 
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            phits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if phits:
                self.player.pos.y = phits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = phits[0].speed*1.5
        

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            # when the player collides with a mob, its score decreases by 1. 
            mhits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if mhits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                self.score -= 1
                if self.player.rect.bottom >= mhits[0].rect.top - 1:
                    self.player.rect.top = mhits[0].rect.bottom

        # elif self.player.vel.y <= 0:
        #     jhits = pg.sprite.spritecollide(self.player, self.all_jumpPlatforms, True)
        #     if jhits:
        #         self.player.acc.y = 5
        #         self.player.vel.y = 0
        #         if self.player.rect.bottom >= mhits[0].rect.top - 1:
        #             self.player.rect.top = mhits[0].rect.bottom

        
                
        # when the player comes into contact with a coin, the coin will disappear and the player's coin count will go up. 
        chits = pg.sprite.spritecollide(self.player, self.all_Coins, True)
        if chits:
            print("i got a coin!")
            self.coins += 1
        
        # using the boundary class, whenever the player's x and y position meets a boundary, their score will tick down by 1 point each second.
        bhits = pg.sprite.spritecollide(self.player, self.all_Boundaries, False)
        if bhits: 
            if self.player.cd.delta == 1:
                print (self.player.cd.delta)
                self.player.cd.event_reset()
                self.score -= 1
                print ("this is working...")
        # when the player's score reaches 0, they will be teleported back to their starting position
        # I was trying to get it to display a message about how the person playing had lost and clear all the platforms, but I never got it to work.
        if self.score == 0:
            self.draw_text(" UH OH, YOU LOST ", 36, RED, WIDTH/2, HEIGHT/2)
            self.player.pos = vec(WIDTH/2, HEIGHT*3/4)
            self.score = 10
            

        
            

        # when the player's score is 0, their position resets to the starting position and their score resets back to ten. 
        # if self.score == 0:
        #     self.draw_text ("UH OH, YOU LOST", 36, RED, WIDTH/2, HEIGHT/2)
        #     self.player.pos = vec(WIDTH/2, HEIGHT*3/4)
        #     self.score = 10



                
                


    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("Coins: " + str(self.coins), 22, WHITE, WIDTH/2, HEIGHT/20)
        # buffer - after drawing everything, flip displayd
        pg.display.flip()
    
    # this allows us to draw text in the window
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()
