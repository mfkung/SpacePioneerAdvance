import arcade
import random
import math
from random import randint
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

class Background(arcade.Sprite):
    def setup(self, x, bottom ):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.center_x = 240
        self.bottom = bottom
    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT

class Explosion(arcade.Sprite):
    def setup(self, x, y):
        self.center_x = x
        self.center_y = y  

class Potion(arcade.Sprite):
    def update(self):
        self.center_y -= 2     

class Falling(arcade.Sprite):
    def update(self):
        super().update()
        self.center_y -= 2

class Particle(arcade.Sprite):
    def update(self):
        super().update()
        self.center_y -= 0.5

class Beam(arcade.Sprite):
    def setup(self, x, y ):
        self.center_x = x
        self.top = y
        self.pos_y = 480
    def update(self):
        if self.center_y > self.pos_y:
            self.center_y -= 3
            
        
        

            