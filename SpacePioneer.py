import arcade
import random
import math
from random import randint
from models import Player, Laser
from enemy import Enemy1, Laser_E, Enemy2, Boss1
from misc import Background, Explosion, Potion, Falling, Particle, Beam
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SPRITE_SCALING = 0.6
INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1
GAME_OVER = 2
CLEAR = 3
MAX_ENEMY1 = 4
MAX_ENEMY2 = 1
MAX_HP = 3
MAX_HP2 = 4
LASER_E_SPEED = 4


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.background = arcade.load_texture("images/BGf.png")
        self.current_state = INSTRUCTIONS_PAGE_0
        self.set_mouse_visible(False)
        self.score = 0
        self.counter = 0
        self.Enemy_Health = 3
        self.Enemy2_Health = 5
        self.BOSS1_Health = 100
        self.beam_duration = 0
        self.beam_state = False
        #self.cure = 0
        self.blast_time = 0
        self.particle_time = 0
        self.game_over = False
        self.instructions = []
        texture = arcade.load_texture("images/intro2.png")
        self.instructions.append(texture)

    def setup(self):
        # Set background
        self.background_list = arcade.SpriteList()
        background = Background("images/BGf.png", SPRITE_SCALING)
        background.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_list.append(background)
        background = Background("images/BGf.png", SPRITE_SCALING)
        background.setup(SCREEN_WIDTH, 0)
        self.background_list.append(background)
    # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.enemy1_list = arcade.SpriteList()
        self.enemy2_list = arcade.SpriteList()
        self.boss1_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.laser_e_list = arcade.SpriteList()
        self.boss_beam = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.cure_list = arcade.SpriteList()
        self.blast_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()
    # Set player
        self.level = 1
        if self.level == 1:
            self.player = Player("images/Player/rocket2.png", SPRITE_SCALING)
            self.player.setup(SCREEN_WIDTH / 2, 60, self.laser_list)
            self.player.level(1)
            self.player_list.append(self.player)
            self.lives = MAX_HP
        elif self.level == 2:
            self.player = Player("images/Player/rocket2.png", SPRITE_SCALING)
            self.player.setup(SCREEN_WIDTH / 2, 60, self.laser_list)
            self.player.level(2)
            self.player_list.append(self.player)
            self.lives = MAX_HP+"2"
    # Set life
        cur_pos = SCREEN_WIDTH - 120
        for i in range(self.lives):
            life = arcade.Sprite("images/Player/lives.png", SPRITE_SCALING)
            life.center_x = cur_pos + life.width
            life.center_y = SCREEN_HEIGHT - 50
            cur_pos += life.width
            self.life_list.append(life)

    # Set asteroid
        image_list = ("images/Asteroid/Giant/Giant1.png",
                      "images/Asteroid/Giant/Giant2.png",
                      "images/Asteroid/Giant/Giant3.png",
                      "images/Asteroid/Giant/Giant4.png")
        for i in range(100):
            image_no = random.randrange(4)
            asteroid_sprite = Falling(image_list[image_no], SPRITE_SCALING * 1.5)
            asteroid_sprite.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT * 50)
            asteroid_sprite.center_x = random.randrange(SCREEN_WIDTH - 10)
            asteroid_sprite.change_angle = (random.random() - 0.5) * 1.4
            asteroid_sprite.size = 3
            self.asteroid_list.append(asteroid_sprite)

    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, page_texture.width, page_texture.height, page_texture, 0)

    def draw_game_over(self):

        output = "Game Over"
        arcade.draw_text(output, 80, 360, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 140, 310, arcade.color.WHITE, 24)

        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 205, 280, arcade.color.WHITE, 14)

    def draw_clear_stage(self):
        arcade.set_background_color(arcade.color.BLACK)
        output = "Congratulation!"
        arcade.draw_text(output, 24, 360, arcade.color.WHITE, 54)

        output = "Stage 1 cleared"
        arcade.draw_text(output, 140, 310, arcade.color.WHITE, 24)

        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 180, 280, arcade.color.WHITE, 14)



    def draw_game(self):
        self.all_sprites_list.draw()
        self.player_list.draw()
        self.laser_list.draw()
        self.asteroid_list.draw()
        self.laser_e_list.draw()
        self.boss_beam.draw()
        self.blast_list.draw()
        self.cure_list.draw()
        self.life_list.draw()
        self.particle_list.draw()
        output = "Score: {}".format(self.score)
        arcade.draw_text(output, 10, 620, arcade.color.WHITE, 14)

        if self.score >= 100 and self.score < 105:
            output = "LEVEL UP"
            arcade.draw_text(output, 100, SCREEN_HEIGHT/2, arcade.color.YELLOW, 54)


        output = f"Level: {self.level}"
        arcade.draw_text(output, 10, 35, arcade.color.WHITE, 14)


        for enemy in self.enemy1_list:
            enemy.laser_e_list.draw()
        self.enemy1_list.draw()
        for enemy in self.enemy2_list:
            enemy.laser_e_list.draw()
        self.enemy2_list.draw()
        for enemy in self.boss1_list:
            enemy.boss_beam.draw()
        self.boss1_list.draw()

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == GAME_OVER:
            self.draw_game_over()
        else:
            self.draw_clear_stage()

    # Key setting
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
            self.score = 0
            self.counter = 0
            self.beam_duration = 0
            self.BOSS1_Health = 100

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

                enemy_sprite = Falling(image_list[image_no], SPRITE_SCALING * 1.5)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = randint(1, 2)
                self.asteroid_list.append(enemy_sprite)

    def particle_asteroid(self, asteroid: Particle):
       # print("split")
        x = asteroid.center_x
        y = asteroid.center_y

        if asteroid.size == 3:
            for i in range(9):
                image_no = random.randrange(2)
                image_list = ["images/Particle/testParticle2.png",
                              "images/Particle/testParticle3.png"]

                enemy_sprite = Particle(image_list[image_no], SPRITE_SCALING)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                self.particle_list.append(enemy_sprite)

        elif asteroid.size == 2:
            for i in range(6):
                image_no = random.randrange(2)
                image_list = ["images/Particle/testParticle2.png",
                              "images/Particle/testParticle3.png"]

                enemy_sprite = Particle(image_list[image_no], SPRITE_SCALING)
                enemy_sprite.center_y = y
                enemy_sprite.center_x = x
                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.particle_list.append(enemy_sprite)

    def particle_enemy(self, enemy: Particle):
       # print("split")
        x = enemy.center_x
        y = enemy.center_y

        for i in range(9):
            image_no = random.randrange(2)
            image_list = ["images/Particle/testParticle4.png",
                          "images/Particle/testParticle5.png"]

            enemy_sprite = Particle(image_list[image_no], SPRITE_SCALING)
            enemy_sprite.center_y = y
            enemy_sprite.center_x = x
            enemy_sprite.change_x = random.random() * 2.5 - 1.25
            enemy_sprite.change_y = random.random() * 2.5 - 1.25
            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            self.particle_list.append(enemy_sprite)

    def particle_self(self, player: Particle):
       # print("split")
        x = player.center_x
        y = player.center_y

        for i in range(15):
            image_no = random.randrange(2)
            image_list = ["images/Particle/testParticle.png",
                          "images/Particle/testParticle1.png"]

            my_sprite = Particle(image_list[image_no], SPRITE_SCALING)
            my_sprite.center_y = y
            my_sprite.center_x = x
            my_sprite.change_x = random.random() * 2.5 - 1
            my_sprite.change_y = random.random() * 2.5 - 1
            my_sprite.change_angle = (random.random() - 0.5) * 2
            self.particle_list.append(my_sprite)

    def update(self, delta):
        if self.current_state == GAME_RUNNING:
            if not self.game_over:
                self.background_list.update()
                self.all_sprites_list.update()
                self.player_list.update()
                self.asteroid_list.update()
                self.laser_list.update()
                self.boss_beam.update()
                self.cure_list.update()
                self.life_list.update()
                self.particle_list.update()
                for enemy in self.enemy1_list:
                    enemy.update(delta)
                for enemy in self.enemy2_list:
                    enemy.update(delta)
                for enemy in self.boss1_list:
                    enemy.update(delta)    
                for asteroid in self.asteroid_list:
                    if asteroid.bottom < -5:
                        asteroid.kill()
            ##### SPAWN ENEMY1 #####            
                if self.counter % 300 == 0 and len(self.enemy1_list) < MAX_ENEMY1 and self.counter <= 5400:
                    enemy = Enemy1("images/Enemy/spaceship1.png", SPRITE_SCALING)
                    choice = [60, 100, 140, 180, 220,
                              260, 300, 340, 380, 420, 460]
                    enemy.setup(choice.pop(random.randrange(len(choice))),SCREEN_HEIGHT + 20,  self.laser_e_list)
                    choice.remove(random.choice(choice))
                    self.enemy1_list.append(enemy)

                for enemy in self.enemy1_list:
                    if self.counter % 90 == 0:
                        laser_e = arcade.Sprite("images/Enemy/laser2.png")
                        laser_e.center_x = enemy.center_x
                        laser_e.top = enemy.bottom
                        laser_e.change_y = -4
                        self.laser_e_list.append(laser_e)
                self.laser_e_list.update()
            ##### SPAWN ENEMY2 #####
                if self.counter >= 2400:
                    if self.counter % 400 == 0 and len(self.enemy2_list) < MAX_ENEMY2 and self.counter <= 5400:
                        enemy = Enemy2(
                            "images/Enemy/spaceship2.png", SPRITE_SCALING / 5.5)
                        choice = [60, 100, 140, 180, 220,
                                  260, 300, 340, 380, 420, 460]
                        spawn_x = randint(0, len(choice) - 1)
                        enemy.setup(choice.pop(random.randrange(
                            len(choice))), SCREEN_HEIGHT + 20,  self.laser_e_list)
                        choice.remove(random.choice(choice))
                        self.enemy2_list.append(enemy)

                for enemy in self.enemy2_list:
                    start_x = enemy.center_x
                    start_y = enemy.center_y

                    # Get the destination location for the laser
                    dest_x = self.player.center_x
                    dest_y = self.player.center_y

                    # The laser will travel.
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)
                    enemy.angle = math.degrees(angle) + 90
                    if self.counter % 95 == 0:
                        laser_e = arcade.Sprite("images/Enemy/laser2.png")
                        laser_e.center_x = start_x
                        laser_e.center_y = start_y
                        laser_e.angle = math.degrees(angle) + 90
                        laser_e.change_x = math.cos(angle) * LASER_E_SPEED
                        laser_e.change_y = math.sin(angle) * LASER_E_SPEED
                        self.laser_e_list.append(laser_e)

            #####  SPAWN POTION #####
                if self.counter % 2000 == 0:
                    self.cure = Potion("images/Health.png",SPRITE_SCALING / 1.5)
                    self.cure.center_x = random.randrange(SCREEN_WIDTH)
                    self.cure.center_y = random.randrange(
                        SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
                    self.cure_list.append(self.cure)

            #####  SPAWN BOSS #####
                if self.counter == 5600:
                    boss1 = Boss1("images/Enemy/destroyer.png",SPRITE_SCALING / 1.5)
                    boss1.setup(randint(220, 260), SCREEN_HEIGHT + 20, self.boss_beam, self.beam_state)
                    self.boss1_list.append(boss1)
                self.beam_duration += 1

                for boss1 in self.boss1_list:
                    if self.counter % 90 == 0:
                        boss_laser = arcade.Sprite("images/Enemy/laser2.png")
                        boss_laser.center_x = boss1.center_x -60
                        boss_laser.top = boss1.bottom
                        boss_laser.change_y = -8
                        self.boss_beam.append(boss_laser)

                    if self.counter % 90 == 0:
                        boss_laser = arcade.Sprite("images/Enemy/laser2.png")
                        boss_laser.center_x = boss1.center_x +60
                        boss_laser.top = boss1.bottom
                        boss_laser.change_y = -8
                        self.boss_beam.append(boss_laser)

                    if self.counter in [7100, 9100, 11100, 13100]:
                        self.beam_state = True
                        beam = Beam("images/test.png", SPRITE_SCALING)
                        beam.setup(boss1.center_x, boss1.center_y - 100)
                        self.boss_beam.append(beam)
                        self.boss_beam.update()

                    elif self.beam_duration in [7600, 9600, 11600, 13600]:
                        for laser in self.boss_beam:
                            laser.kill()
                            self.beam_state = False
               # print(self.beam_state)
        #################   HIT CHECK ##################
                ##### KILL ASTEROID ######
                for laser in self.laser_list:
                    asteroids = arcade.check_for_collision_with_list(laser, self.asteroid_list)
                    if len(asteroids) > 0:
                        laser.kill()
                        for asteroid in asteroids:
                            asteroid.kill()
                            for i in range(1, 6):
                                blast = Explosion("images/Explosion/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(asteroid.center_x,asteroid.center_y)
                                self.blast_list.append(blast)
                            self.split_asteroid(asteroid)
                            self.particle_asteroid(asteroid)

                if not self.player.respawning:
                    ##### ASTEROID HIT PLAYER  #####
                    asteroids = arcade.check_for_collision_with_list(self.player, self.asteroid_list)

                    if len(asteroids) > 0:
                        if self.lives > 0:
                            print("-1 live")
                            self.particle_self(self.player)
                            self.lives -= 1
                            self.life_list.pop().kill()
                            self.player.respawn()
                            asteroids[0].kill()
                            print(self.lives)

                ##### POTION HIT PLAYER  #####
                    potion = arcade.check_for_collision_with_list(self.player, self.cure_list)

                    if len(potion) > 0:
                        if self.lives > 0 and self.lives < 3:
                            self.lives += 1
                            print(self.lives)
                            potion[0].kill()
                            for i in range(self.lives - 1):
                                if self.lives > 1:
                                    self.life_list.pop().kill
                            cur_pos = SCREEN_WIDTH - 120
                            for i in range(self.lives):
                                life = arcade.Sprite("images/Player/lives.png", SPRITE_SCALING)
                                life.center_x = cur_pos + life.width
                                life.center_y = SCREEN_HEIGHT - 50
                                cur_pos += life.width
                                self.life_list.append(life)
                                self.life_list.update()
                        elif self.lives == MAX_HP:
                            self.score += 3
                            potion[0].kill()
                ##### LASER HIT PLAYER  #####
                    laser = arcade.check_for_collision_with_list(self.player, self.laser_e_list)

                    if len(laser) > 0:
                        if self.lives > 0:
                            print("-1 live")
                            self.particle_self(self.player)
                            self.lives -= 1
                            self.player.respawn()
                            laser[0].kill()
                            self.life_list.pop().kill()
                            print(self.lives)

                ##### LASER-BEAM HIT PLAYER  #####
                    laser = arcade.check_for_collision_with_list(self.player, self.boss_beam)

                    if len(laser) > 0:
                        if self.lives > 0:
                            print("-1 live")
                            self.particle_self(self.player)
                            self.lives -= 1
                            self.player.respawn()
                            self.life_list.pop().kill()
                            print(self.lives)
                ##### BOSS HIT Asteroids  #####
                    for enemy in self.boss1_list:
                        asteroids = arcade.check_for_collision_with_list(enemy, self.asteroid_list)
                    if len(asteroids) > 0:
                        for asteroid in asteroids:
                            asteroid.kill()
                            for i in range(1, 6):
                                blast = Explosion("images/Explosion/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(asteroid.center_x,asteroid.center_y)
                                self.blast_list.append(blast)
                            
                ##### LASER-BEAM HIT Asteroids  #####
                    for beam in self.boss_beam:
                        asteroids = arcade.check_for_collision_with_list(beam, self.asteroid_list)
                    if len(asteroids) > 0:
                        for asteroid in asteroids:
                            asteroid.kill()
                            for i in range(1, 6):
                                blast = Explosion("images/Explosion/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(asteroid.center_x,asteroid.center_y)
                                self.blast_list.append(blast)
                            
            ##### KILL ENEMY1 #####
                for laser in self.laser_list:
                    player_hits = arcade.check_for_collision_with_list(laser, self.enemy1_list)
                    if len(player_hits) > 0:
                        laser.kill()
                        for enemy in player_hits:
                            self.Enemy_Health -= 1
                            for i in range(1, 10):
                                blast = Explosion("images/Explosion/images/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(enemy.center_x, enemy.center_y)
                                self.blast_list.append(blast)
                            if self.Enemy_Health == 1:
                                enemy.kill()
                                self.particle_enemy(enemy)
                                self.score += 5
                                self.Enemy_Health = 3
            ##### KILL ENEMY2 #####
                for laser in self.laser_list:
                    player_hits = arcade.check_for_collision_with_list(laser, self.enemy2_list)
                    if len(player_hits) > 0:
                        laser.kill()
                        for enemy in player_hits:
                            self.Enemy2_Health -= 1
                            #print(self.Enemy2_Health)
                            for i in range(1, 10):
                                blast = Explosion("images/Explosion/images/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(enemy.center_x, enemy.center_y)
                                self.blast_list.append(blast)

                            if self.Enemy2_Health == 1:
                                enemy.kill()
                                self.particle_enemy(enemy)
                                self.score += 8
                                self.Enemy2_Health = 5
            ##### KILL BOSS1 #####
                for laser in self.laser_list:
                    player_hits = arcade.check_for_collision_with_list(laser, self.boss1_list)
                    if len(player_hits) > 0:
                        laser.kill()
                        for enemy in player_hits:
                            self.BOSS1_Health -= 1
                            print(self.BOSS1_Health)
                            for i in range(1, 10):
                                blast = Explosion("images/Explosion/images/explosion" + str(i) + ".png", SPRITE_SCALING)
                                blast.setup(enemy.center_x, enemy.center_y)
                                self.blast_list.append(blast)

                            if self.BOSS1_Health == 1:
                                enemy.kill()
                                self.particle_enemy(enemy)
                                self.score += 1000
                                self.current_state = CLEAR  
            #####  LEVEL UP  #####
                if self.score >= 100:
                    self.player.level = 2  
                    
            ##### DELAY BLAST #####
                self.blast_time += delta
                self.particle_time += delta
                if self.blast_time > 0.005:
                    self.blast_time = 0
                    if len(self.blast_list) > 0:
                        self.blast_list[0].kill()

                if self.particle_time > 0.1:
                    self.particle_time = 0
                    if len(self.particle_list) > 0:
                        self.particle_list[0].kill()
            
            ##### CHECK GAME OVER #####
                if self.lives == 0:
                    self.current_state = GAME_OVER
                    self.set_mouse_visible(True)

                self.counter += 1



if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()
