import arcade
import random
from models import Player,Falling,Laser
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.7

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.all_sprites_list = None
        self.player_sprite = None
        self.rock_list = None
        self.laser_list = None
        self.background = None
        self.set_mouse_visible(False)
        self.score = 0
        arcade.set_background_color(arcade.color.BLACK)
    
    def Asteroid(self):
       for i in range(100):

            rock = Falling("images/Asteroid1.png", SPRITE_SCALING / 2)
            rock.center_x = random.randrange(SCREEN_WIDTH-10)
            rock.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 50)
            self.all_sprites_list.append(rock)
            self.rock_list.append(rock)

    def setup(self):
        #Set backgound
        self.background = arcade.load_texture("images/BG.jpg")
        #sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        #Set player
        self.player = Player("images/rocket2.png", SPRITE_SCALING)
        self.player.setup(SCREEN_WIDTH/2, 60, self.all_sprites_list,self.rock_list, self.score)
        self.all_sprites_list.append(self.player)
        self.laser = Laser("images/laser1.png", SPRITE_SCALING * 1.5)
        #set asteroid
        self.Asteroid() 

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.all_sprites_list.draw()
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
    #Key setting
    def on_key_press(self, key, key_modifiers):
        self.player.on_key_press(key, key_modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    

    def update(self, delta):
        self.all_sprites_list.update()
        
        
        '''hit_list = \
            arcade.check_for_collision_with_list(self.player,
                                                 self.rock_list)
        if hit_list:
            player.kill()'''

 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()