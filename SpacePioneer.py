import arcade
from models import Player
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.5


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background = None
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)
       
    def setup(self):
        #Set backgound
        self.background = arcade.load_texture("images/BG.jpg")
        #sprite lists
        self.all_sprites_list = arcade.SpriteList()
        #Set rocket
        self.player = Player("images/rocket.png", SPRITE_SCALING)
        self.player.setup(SCREEN_WIDTH/2, 70, self.all_sprites_list)
        self.all_sprites_list.append(self.player)

   
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player.draw()
#    def update(self, delta):
#        self.player.update(delta)
        
        
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()