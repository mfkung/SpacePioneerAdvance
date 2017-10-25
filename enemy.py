import arcade.key
import random
import math
from random import randint
from models import Player
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
MOVEMENT_SPEED = 2
LASER_SPEED = 10
SPRITE_SCALING = 0.7

class Laser_E(arcade.Sprite):
    def setup(self, x, y):
        self.center_x = x
        self.top = y
    def update(self):
        self.center_y -= LASER_SPEED-8

class Enemy1(arcade.Sprite):
    def setup(self, x, y,  laser_e_list):   
        self.laser_e_list = laser_e_list
        self.center_x = x
        self.center_y = y
        choice_y = [475,495,525,555]
        self.pos_y = choice_y.pop(random.randrange(len(choice_y)))
        self.frame_count = 0 

    def update(self,delta):
        self.frame_count += 1
        if self.center_y > self.pos_y:
            self.center_y -= 3

class Enemy2(arcade.Sprite):
    def setup(self, x, y,  laser_e_list):   
        self.laser_e_list = laser_e_list
        self.center_x = x
        self.center_y = y
        choice_y = [495,525]
        self.pos_y = choice_y.pop(random.randrange(len(choice_y)))
        self.frame_count = 0 


    def update(self,delta):
        self.frame_count += 1
        if self.center_y > self.pos_y:
            self.center_y -= 3

class Boss1(arcade.Sprite):
    def setup(self, x, y,  boss_beam, beam_state):   
        self.boss_beam = boss_beam
        self.beam_state = beam_state
        self.center_x = x
        self.center_y = y
        self.pos_y = 550
        self.frame_count = 0 


    def update(self,delta):
        self.frame_count += 1
        self.center_x += self.change_x
        if self.center_y > self.pos_y:
            self.center_y -= 3

                 
        


