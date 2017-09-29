import arcade.key



SCREEN_HEIGHT = 480
SCREEN_WIDTH = 640

MOVEMENT_SPEED = 4


#KEY_OFFSET = {arcade.key.UP: DIR_UP,
#              arcade.key.DOWN: DIR_DOWN,
#              arcade.key.RIGHT: DIR_RIGHT,
#              arcade.key.LEFT: DIR_LEFT}

class Player(arcade.Sprite):
    def setup(self, x, y, all_sprites_list):
        self.all_sprites_list = all_sprites_list
        self.center_x = x
        self.center_y = y        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.change_x = 0

    
   
    def update(self, delta):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

      