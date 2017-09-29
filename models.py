import arcade.key

SPRITE_SCALING = 0.5

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 500

MOVEMENT_SPEED = 3

BULLET_TIME = 0.25
#KEY_OFFSET = {arcade.key.UP: DIR_UP,
#              arcade.key.DOWN: DIR_DOWN,
#              arcade.key.RIGHT: DIR_RIGHT,
#              arcade.key.LEFT: DIR_LEFT}

class Player(arcade.Sprite):
    def setup(self, x, y, all_sprites_list):
        self.all_sprites_list = all_sprites_list
        self.bullet_list = arcade.SpriteList()
        self.center_x = x
        self.center_y = y
        self.wait_time = 0

    

      