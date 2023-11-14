# This file was created by: Chris Cozort
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 


from math import floor

# game settings 
WIDTH = 1024
HEIGHT = 768
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# the list to draw all the platforms from and their categories. 
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal"),
                 (125, HEIGHT - 350, 100, 20, "normal"),
                 (500, 250, 100, 20, "normal"),
                 (750, 200, 50, 20, "normal")]

# JUMPPLATFORM_LIST = [(512, 384, 100, 30, "normal")]
# the list that draws all the mobs and how they move
MOB_LIST = [(400, 400, 25, 25, "moving vertically"),
             (600, 400, 25, 25, "moving vertically"),
            (850, 150, 25, 25, "moving horizontally"),
            (800, 200, 25, 25, "moving horizontally"),]
            
# tells the code where to place the boundary. 
BOUND_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal")]

# tells the code where to place the coin. 
COIN_LIST = [(760, 160, 15, 15, "moving")]