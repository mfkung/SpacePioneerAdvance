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
        if self.center_x < -100 or self.center_x > 1500 or \
                self.center_y > 1100 or self.center_y < -100:
            self.kill()
class Laser_E(arcade.Sprite):
    def update(self):
        self.center_y -= LASER_SPEED-5
        if self.center_x < -100 or self.center_x > 1500 or \
                self.center_y > 1100 or self.center_y < -100:
            self.kill()

class Player(arcade.Sprite):
    def setup(self, x, y, all_sprites_list, rock_list, enemy_list, score):
        self.all_sprites_list = all_sprites_list
        self.laser_list = arcade.SpriteList()
        self.rock_list = rock_list
        self.enemy_list = enemy_list
        self.center_x = x
        self.center_y = y        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            laser = Laser("images/laser1.png", SPRITE_SCALING * 1.5)
            laser.center_x = self.center_x
            laser.bottom = self.top -20

           
            self.all_sprites_list.append(laser)
            self.laser_list.append(laser)    

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.LEFT:
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

        for laser in self.laser_list:
            hit_list = arcade.check_for_collision_with_list(laser,
                                                            self.rock_list)
            if len(hit_list) > 0:
                laser.kill()
            for rock in hit_list:
                rock.kill()
                #score += 1
        for laser in self.laser_list:
            hit_list = arcade.check_for_collision_with_list(laser,
                                                            self.enemy_list)
            if len(hit_list) > 0:
                laser.kill()
            for enemy in hit_list:
                enemy.kill() 
        for laser in self.laser_list:         
            if laser.top > 660:
                laser.kill()  

####    Asteroid ####
class Falling(arcade.Sprite):
    def update(self):
        self.center_y -= 2
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT

####   Enemy1 ####
class Enemy1(arcade.Sprite):
    def setup(self, x, y, all_sprites_list):
        self.all_sprites_list = all_sprites_list
        self.laser_list = arcade.SpriteList()
        self.center_x = x
        self.center_y = y
        self.center_y -= random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 50)
        self.center_x -= random.randrange(SCREEN_WIDTH-10)

        self.wait_time = 0
        self.frame_count = 0 

    def shoot(self):
        laser = Laser_E("images/laser2.png", SPRITE_SCALING * 1.5)
        laser.center_x = self.center_x
        laser.bottom = self.top -20
        
        
        laser.center_x = self.center_x
        laser.top = self.bottom
        
        
        self.laser_list.append(laser)

    def update(self):
        self.frame_count += 1
        self.center_y -= 3
        if self.top < 620:
            self.top = 620
        
        self.laser_list.update()
        if self.frame_count % 75 == 0:
            self.shoot()
        for laser in self.laser_list:         
            if laser.bottom < 0:
                laser.kill()