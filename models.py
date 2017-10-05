import arcade.key
from random import randint

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
MOVEMENT_SPEED = 5
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

class Player(arcade.Sprite):
    def setup(self, x, y, all_sprites_list, rock_list, score):
        self.all_sprites_list = all_sprites_list
        self.laser_list = arcade.SpriteList()
        self.rock_list = rock_list
        self.center_x = x
        self.center_y = y        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            laser = Laser("images/laser1.png", SPRITE_SCALING * 1.5)
            laser.center_x = self.center_x
            laser.bottom = self.top

           
            self.all_sprites_list.append(laser)
            self.laser_list.append(laser)    

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0
    
    def update(self):
        self.center_x += self.change_x
   

        if self.left < -5:
            self.left = -5
        if self.right > SCREEN_WIDTH+5:
            self.right = SCREEN_WIDTH+5

        for laser in self.laser_list:
            hit_list = arcade.check_for_collision_with_list(laser,
                                                            self.rock_list)
            if len(hit_list) > 0:
                laser.kill()
            for rock in hit_list:
                rock.kill()
                #score += 1
####    Asteroid ####
class Falling(arcade.Sprite):
    def update(self):
        self.center_y -= 3
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT



     

      