import arcade
import random
from random import randint
from models import Player,Falling,Laser,Enemy1
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.7
INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.current_state = INSTRUCTIONS_PAGE_0
        self.all_sprites_list = None
        self.player_sprite = None
        self.rock_list = None
        self.laser_list = None
        self.background = None
        self.enemy_list = None
        self.set_mouse_visible(False)
        self.score = 0
        self.game_over = False
        
        self.instructions = []
        
        texture = arcade.load_texture("images/intro2.png")
        self.instructions.append(texture)
        

    def setup(self):
        #Set backgound
        self.background = arcade.load_texture("images/BGf.png")
        #Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        #Set player
        self.player = Player("images/rocket2.png", SPRITE_SCALING)
        self.player.setup(SCREEN_WIDTH/2, 60, self.all_sprites_list,self.rock_list, self.enemy_list ,self.score)
        self.all_sprites_list.append(self.player)
        #Set enemy1
        for i in range(25):
            self.enemy1_sprite = Enemy1("images/spaceship1.png", SPRITE_SCALING)
            self.enemy1_sprite.setup(randint(40,440), 0 , self.all_sprites_list)
            self.enemy1_sprite.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 25)
            self.enemy1_sprite.center_x = randint(40,440)
            self.all_sprites_list.append(self.enemy1_sprite)
            self.enemy_list.append(self.enemy1_sprite)
        #Set asteroid
        image_list = ("images/Asteroid/Giant/Giant1.png",
                      "images/Asteroid/Giant/Giant2.png",
                      "images/Asteroid/Giant/Giant3.png",
                      "images/Asteroid/Giant/Giant4.png")
        for i in range(100):
            image_no = random.randrange(4)
            asteroid_sprite = Falling(image_list[image_no], SPRITE_SCALING*1.5)

            asteroid_sprite.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 50)
            asteroid_sprite.center_x = random.randrange(SCREEN_WIDTH-10)

            asteroid_sprite.change_angle = (random.random() - 0.5) * 2
            #asteroid.size = 4
            self.all_sprites_list.append(asteroid_sprite)
            self.rock_list.append(asteroid_sprite)
        
    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
    def draw_game(self):
        self.all_sprites_list.draw()
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 620, arcade.color.WHITE, 14)                                  
        for enemy in self.enemy_list:
            enemy.laser_list.draw()
        self.enemy_list.draw()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        
    #Key setting
    def on_key_press(self, key, key_modifiers):
        self.player.on_key_press(key, key_modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.current_state == INSTRUCTIONS_PAGE_0:    
            self.current_state = GAME_RUNNING
            self.setup()

    def update(self, delta):
        if self.current_state == GAME_RUNNING:
            self.all_sprites_list.update()
            hit_list = \
                arcade.check_for_collision_with_list(self.player,
                                                    self.rock_list)
            for rock in hit_list:
                rock.kill()
                self.game_over = True
                print("Game over")
                exit()
            '''hit_list2 = \
                arcade.check_for_collision_with_list(self.player,
                                                    self.laser_list)
            for laser in hit_list2:
                laser.kill()
                self.game_over = True
                print("Game over")
                exit()    '''
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()