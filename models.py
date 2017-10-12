import arcade.key
import random
from random import randint

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
MOVEMENT_SPEED = 6
LASER_SPEED = 10
SPRITE_SCALING = 0.7

#KEY_OFFSET = {arcade.key.UP: DIR_UP,
#              arcade.key.DOWN: DIR_DOWN,
#              arcade.key.RIGHT: DIR_RIGHT,
#              arcade.key.LEFT: DIR_LEFT}
class Laser(arcade.Sprite):
    def update(self):
        self.center_y += LASER_SPEED

class Player(arcade.Sprite):
    def setup(self, x, y,  laser_list):
        self.laser_list = laser_list
        self.center_x = x
        self.center_y = y    
        self.respawning = 0  
    def respawn(self):
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 60
        self.angle = 0
    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -MOVEMENT_SPEED
        elif not self.respawning and key == arcade.key.SPACE:
            laser = Laser("images/laser1.1.png", SPRITE_SCALING * 1.5)
            laser.center_x = self.center_x
            laser.bottom = self.top -20
            self.laser_list.append(laser)    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.change_y = 0   
    
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < -5:
            self.left = -5
        if self.right > SCREEN_WIDTH+5:
            self.right = SCREEN_WIDTH+5
        if self.bottom < 5:
            self.bottom = 5
        if self.top > SCREEN_HEIGHT-5:
            self.top = SCREEN_HEIGHT-5 

        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning / 500
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 1

        for laser in self.laser_list:         
            if laser.top > 645:
                laser.kill()  


        
