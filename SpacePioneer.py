import arcade
import random
import math
from random import randint
from models import Player,Laser,Enemy1,Falling
from misc import Background, Explosion , Potion
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.6
INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1
GAME_OVER = 2
MAX_ENEMY1 = 5

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background = arcade.load_texture("images/BGf.png")
        self.current_state = INSTRUCTIONS_PAGE_0
        self.set_mouse_visible(False)
        self.score = 0
        self.counter = 0
        self.lives = 3
        #self.cure = 0
        self.blast_time = 0
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
        self.cure_list = arcade.SpriteList()
        self.blast_list = arcade.SpriteList()
    #Set player
        self.player = Player("images/rocket2.png", SPRITE_SCALING)
        self.player.setup(SCREEN_WIDTH/2, 60, self.laser_list)
        self.all_sprites_list.append(self.player)
        self.lives = 3
    #Set life
        cur_pos = SCREEN_WIDTH-120
        for i in range(self.lives):
            life = arcade.Sprite("images/lives.png", SPRITE_SCALING)
            life.center_x = cur_pos + life.width
            life.center_y = SCREEN_HEIGHT -50
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.life_list.append(life)
    
        
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
            self.asteroid_list.append(asteroid_sprite)
    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
    def draw_game_over(self):

        output = "Game Over"
        arcade.draw_text(output, 80 , 360 , arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 140, 310, arcade.color.WHITE, 24)
                                          
    def draw_game(self):
        self.all_sprites_list.draw()
        self.laser_list.draw()
        self.asteroid_list.draw()
        self.laser_e_list.draw()
        self.blast_list.draw()
        self.cure_list.draw()
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 620, arcade.color.WHITE, 14)                                  
        for enemy in self.enemy_list:
            enemy.laser_e_list.draw()
        self.enemy_list.draw()

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()

        
    #Key setting
    def on_key_press(self, key, key_modifiers):
        self.player.on_key_press(key, key_modifiers)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.current_state == INSTRUCTIONS_PAGE_0:    
            self.current_state = GAME_RUNNING
            self.setup()
        elif self.current_state == GAME_OVER:
            self.setup()
            self.current_state = GAME_RUNNING  

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
                if self.counter % 75 == 0 and len(self.enemy_list) < MAX_ENEMY1:

                    self.enemy1_sprite = Enemy1("images/spaceship1.png", SPRITE_SCALING)
                    choice = [60, 100, 140, 180, 220, 260, 300, 340, 380, 420, 460]
                    spawn_x = randint(0, len(choice)-1)
                    self.enemy1_sprite.setup(choice.pop(random.randrange(len(choice))), 0 ,  self.laser_e_list)
                    self.enemy1_sprite.center_y = SCREEN_HEIGHT + 20
                    #self.enemy1_sprite.center_x = randint(40,440)
                    choice.remove(random.choice(choice))
                    self.enemy_list.append(self.enemy1_sprite)
                if self.counter == 5:
                    self.cure = Potion("images/Health.png", SPRITE_SCALING)
                    self.enemy1_sprite.center_y = SCREEN_HEIGHT + 20
                    self.cure.center_x = randint(40,400)
                    self.cure_list.append(self.cure)


            #################   HIT CHECK ##################
                for laser in self.laser_list:
                    asteroids = arcade.check_for_collision_with_list(laser, self.asteroid_list)
                    if len(asteroids) > 0:
                        laser.kill()
                        for asteroid in asteroids:
                            asteroid.kill()
                            for i in range(1, 6):
                                    blast = Explosion("images/Explosion/explosion"+str(i)+".png", SPRITE_SCALING)
                                    blast.setup(asteroid.center_x, asteroid.center_y)
                                    self.blast_list.append(blast)
                            self.split_asteroid(asteroid)
                            
                            
                        
                if not self.player.respawning:        
                    asteroids = arcade.check_for_collision_with_list(self.player, self.asteroid_list)
                    
                    if len(asteroids) > 0:
                        if self.lives > 0:
                            for i in range(1, 12):
                                blast = Explosion("images/Explosion/crash/crash"+str(i)+".png", SPRITE_SCALING)
                                blast.setup(self.player.center_x, self.player.center_y)
                                self.blast_list.append(blast)
                            print("-1 live")
                            self.lives -= 1
                            self.player.respawn()
                            asteroids[0].kill()

                            self.life_list.pop().kill()
                        else:
                            self.game_over = True
                            print("game over")
                            #exit()
                    laser = arcade.check_for_collision_with_list(self.player, self.laser_e_list)
                    
                    if len(laser) > 0:
                        if self.lives > 0:
                            for i in range(1, 12):
                                blast = Explosion("images/Explosion/crash/crash"+str(i)+".png", SPRITE_SCALING)
                                blast.setup(self.player.center_x, self.player.center_y)
                                blast.change_angle = (random.random() - 0.5) * 1.4
                                self.blast_list.append(blast)
                            print("-1 live")
                            self.lives -= 1
                            self.player.respawn()
                            laser[0].kill()

                            self.life_list.pop().kill()
                        else:
                            self.game_over = True
                            print("game over")
                            #exit()        
                for laser in self.laser_list:
                    player_hits = arcade.check_for_collision_with_list(laser, self.enemy_list)
                    if len(player_hits) > 0:
                        laser.kill()
                        for enemy in player_hits:
                            enemy.kill()
                            for i in range(1, 10):
                                blast = Explosion("images/Explosion/images/explosion"+str(i)+".png", SPRITE_SCALING)
                                blast.setup(enemy.center_x, enemy.center_y)
                                self.blast_list.append(blast)
                        self.score += 5

                self.blast_time += delta
                if self.blast_time > 0.005 :
                    self.blast_time = 0
                    if len(self.blast_list) > 0:
                        self.blast_list[0].kill()
                self.counter += 1
                if len(self.life_list) == 0:
                    self.current_state = GAME_OVER
                    self.set_mouse_visible(True)



if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()