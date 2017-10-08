import arcade
import random
import math
from random import randint
from models import Player,Laser,Enemy1
from asteroid import Falling
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.6
INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1

class Background(arcade.Sprite):
    def setup(self, x, bottom ):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.center_x = 240
        self.bottom = bottom

    def update(self):
        self.center_y -= 1
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background = arcade.load_texture("images/BGf.png")
        self.current_state = INSTRUCTIONS_PAGE_0
        self.all_sprites_list = None
        self.player_sprite = None
        self.asteroid_list = None
        self.laser_list = None
        self.enemy_list = None
        self.set_mouse_visible(False)
        self.score = 0
        self.counter = 0
        self.lives = 3
        self.game_over = False
        self.instructions = []
        texture = arcade.load_texture("images/intro2.png")
        self.instructions.append(texture)
        

    def setup(self):
        #Set background
        self.background_list = arcade.SpriteList()
        background = Background("images/BGf.png", SPRITE_SCALING)
        background.setup(SCREEN_WIDTH  ,SCREEN_HEIGHT)
        self.background_list.append(background)
        background = Background("images/BGf.png", SPRITE_SCALING)
        background.setup(SCREEN_WIDTH ,0)
        self.background_list.append(background)

        #Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.laser_e_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        #Set player
        self.player = Player("images/rocket2.png", SPRITE_SCALING)
        self.player.setup(SCREEN_WIDTH/2, 60, self.all_sprites_list,self.asteroid_list, self.enemy_list ,self.score, self.laser_list)
        self.all_sprites_list.append(self.player)
        self.lives = 3
        #Set lives
        cur_pos = SCREEN_WIDTH-90
        for i in range(self.lives):
            life = arcade.Sprite("images/rocket2.png", SPRITE_SCALING/2.5)
            life.center_x = cur_pos + life.width
            life.center_y = SCREEN_HEIGHT-30
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.life_list.append(life)
        #Set enemy1
        
        
        if not self.game_over and len(self.enemy_list) < 5:

            self.enemy1_sprite = Enemy1("images/spaceship1.png", SPRITE_SCALING)
            self.enemy1_sprite.setup(randint(40,440), 0 ,  self.laser_e_list)
            self.enemy1_sprite.center_y = SCREEN_HEIGHT + 20
            self.enemy1_sprite.center_x = randint(40,440)
            
            
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

            asteroid_sprite.change_angle = (random.random() - 0.5) * 1.4
            asteroid_sprite.size = 3
            #self.all_sprites_list.append(asteroid_sprite)
            self.asteroid_list.append(asteroid_sprite)
        
    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
    def draw_game(self):
        self.all_sprites_list.draw()
        self.laser_list.draw()
        self.asteroid_list.draw()
        self.laser_e_list.draw()
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 620, arcade.color.WHITE, 14)                                  
        for enemy in self.enemy_list:
            enemy.laser_e_list.draw()
        self.enemy_list.draw()

    def on_draw(self):
        arcade.start_render()
        #arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.background_list.draw()
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
    def split_asteroid(self, asteroid: Falling):
       # print("split")
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 3:
            for i in range(2):
                image_no = random.randrange(2)
                image_list = ["images/Asteroid/Nomal/Normal3.png",
                              "images/Asteroid/Nomal/Normal4.png"]

                enemy_sprite = Falling(image_list[image_no],
                                              SPRITE_SCALING * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = randint(1,2)

                self.asteroid_list.append(enemy_sprite)
       
        elif asteroid.size == 2:
            for i in range(2):
                image_no = random.randrange(2)
                image_list = ["images/Asteroid/Tiny/Tiny1.png",
                              "images/Asteroid/Tiny/Tiny2.png"]

                enemy_sprite = Falling(image_list[image_no],
                                              SPRITE_SCALING * 1.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1


                self.asteroid_list.append(enemy_sprite)

    def update(self, delta):
        self.background_list.update()
        if self.current_state == GAME_RUNNING:
            if not self.game_over:
                for enemy in self.enemy_list:
                    enemy.update(delta)
                self.all_sprites_list.update()
                self.laser_e_list.update()
                for asteroid in self.asteroid_list:         
                    if asteroid.bottom < -5:
                        asteroid.kill()  
                self.asteroid_list.update()
                self.laser_list.update()
                for laser in self.laser_list:
                    asteroids = arcade.check_for_collision_with_list(laser, self.asteroid_list)
                    for asteroid in asteroids:
                        #print("hit")
                        self.split_asteroid(asteroid)
                        asteroid.kill()
                        laser.kill()
                if not self.player.respawning:        
                    asteroids = arcade.check_for_collision_with_list(self.player, self.asteroid_list)
                    
                    if len(asteroids) > 0:
                        if self.lives > 0:
                            print("-1 live")
                            self.lives -= 1
                            self.player.respawn()
                            asteroids[0].kill()

                            self.life_list.pop().kill()
                        else:
                            self.game_over = True
                            print("game over")
                            exit()
                    laser = arcade.check_for_collision_with_list(self.player, self.laser_e_list)
                    
                    if len(laser) > 0:
                        if self.lives > 0:
                            print("-1 live")
                            self.lives -= 1
                            self.player.respawn()
                            laser[0].kill()

                            self.life_list.pop().kill()
                        else:
                            self.game_over = True
                            print("game over")
                            exit()        
                for laser in self.laser_list:
                    player_hits = arcade.check_for_collision_with_list(laser, self.enemy_list)
                    if len(player_hits) > 0:
                        laser.kill()
                        for enemy in player_hits:
                            enemy.kill()
                        self.score += 5
                self.counter += 1
                        
 
if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()