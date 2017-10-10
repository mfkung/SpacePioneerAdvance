import arcade.key
import random
import math
from random import randint
from models import Player
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
MOVEMENT_SPEED = 6
LASER_SPEED = 10
SPRITE_SCALING = 0.7

class Laser_E(arcade.Sprite):
    def setup(self, x, y):
        self.center_x = x
        self.top = y
    def update(self):
        self.center_y -= LASER_SPEED-9

class Enemy1(arcade.Sprite):
    def setup(self, x, y,  laser_e_list):   
        self.laser_e_list = laser_e_list
        self.center_x = x
        self.center_y = y
        choice_y = [460,475,495,525,555]
        self.pos_y = choice_y.pop(random.randrange(len(choice_y)))
        self.frame_count = 0 

    def shoot(self):
        laser_e = Laser_E("images/laser2.png", SPRITE_SCALING * 1.5)
        laser_e.setup(self.center_x,self.center_y)
        self.laser_e_list.append(laser_e)

    def update(self,delta):
        self.frame_count += 1
        if self.center_y > self.pos_y:
            self.center_y -= 3

        
        self.laser_e_list.update()
        if self.frame_count % 75 == 0:
            self.shoot()
        for laser_e in self.laser_e_list:         
            if laser_e.bottom < 0:
                laser_e.kill()

class Enemy2(arcade.Sprite):
    def setup(self, x, y,  laser_e_list):   
        self.laser_e_list = laser_e_list
        self.center_x = x
        self.center_y = y
        choice_y = [460,475,495,525,555]
        self.pos_y = choice_y.pop(random.randrange(len(choice_y)))
        self.frame_count = 0 

    def shoot(self):
        laser_e = Laser_E("images/laser2.png", SPRITE_SCALING * 1.5)
        laser_e.setup(self.center_x,self.center_y)
        self.laser_e_list.append(laser_e)

    def update(self,delta):
        self.frame_count += 1
        if self.center_y > self.pos_y:
            self.center_y -= 3

        
        self.laser_e_list.update()
        if self.frame_count % 75 == 0:
            self.shoot()
        for laser_e in self.laser_e_list:         
            if laser_e.bottom < 0:
                laser_e.kill()
