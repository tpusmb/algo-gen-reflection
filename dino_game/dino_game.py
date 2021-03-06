__author__ = "Rohit Rane"

import random
import os

import pygame
from pygame import *

pygame.init()

FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
SCREEN_SIZE = (width, height) = (600, 150)
FPS = 200
GRAVITY = 0.6

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (235, 235, 235)

HIGH_SCORE = 0
NB_ITERATION = 0

APP_SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Dino Run")

IS_SOUND_ENABLE = False
JUMP_SOUND = pygame.mixer.Sound(os.path.join(FOLDER_ABSOLUTE_PATH, 'sprites', 'jump.wav'))
DIE_SOUND = pygame.mixer.Sound(os.path.join(FOLDER_ABSOLUTE_PATH, 'sprites', 'die.wav'))
CHECKPOINT_SOUND = pygame.mixer.Sound(os.path.join(FOLDER_ABSOLUTE_PATH, 'sprites', 'checkPoint.wav'))


def load_image(name, size_x=-1, size_y=-1, color_key=None):
    fullname = os.path.join(FOLDER_ABSOLUTE_PATH, 'sprites', name)
    loading_image = pygame.image.load(fullname)
    loading_image = loading_image.convert()
    if color_key is not None:
        if color_key is -1:
            color_key = loading_image.get_at((0, 0))
        loading_image.set_colorkey(color_key, RLEACCEL)

    if size_x != -1 or size_y != -1:
        loading_image = pygame.transform.scale(loading_image, (size_x, size_y))

    return loading_image, loading_image.get_rect()


def load_sprite_sheet(sheet_name, nx, ny, scale_x=-1, scale_y=-1, color_key=None):
    fullname = os.path.join(FOLDER_ABSOLUTE_PATH, 'sprites', sheet_name)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    size_x = sheet_rect.width / nx
    size_y = sheet_rect.height / ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * size_x, i * size_y, size_x, size_y))
            current_image = pygame.Surface(rect.size)
            current_image = current_image.convert()
            current_image.blit(sheet, (0, 0), rect)

            if color_key is not None:
                if color_key is -1:
                    color_key = current_image.get_at((0, 0))
                current_image.set_colorkey(color_key, RLEACCEL)

            if scale_x != -1 or scale_y != -1:
                current_image = pygame.transform.scale(current_image, (scale_x, scale_y))

            sprites.append(current_image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


def display_game_over_msg(retry_button_image, game_over_image):
    retry_button_rect = retry_button_image.get_rect()
    retry_button_rect.centerx = width / 2
    retry_button_rect.top = height * 0.52

    game_over_rect = game_over_image.get_rect()
    game_over_rect.centerx = width / 2
    game_over_rect.centery = height * 0.35

    APP_SCREEN.blit(retry_button_image, retry_button_rect)
    APP_SCREEN.blit(game_over_image, game_over_rect)


def extract_digits(number):
    if number > -1:
        digits = []
        while number / 10 != 0:
            digits.append(number % 10)
            number = int(number / 10)

        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


class Dino:
    def __init__(self, dino_id, size_x=-1, size_y=-1):
        self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, size_x, size_y, -1)
        self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, size_y, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width / 15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.is_jumping = False
        self.is_dead = False
        self.is_ducking = False
        self.is_blinking = False
        self.movement = [0, 0]
        self.jump_speed = 11.5
        self.dino_id = dino_id

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)

    def check_bounds(self):
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.is_jumping = False

    def update(self):
        if self.is_jumping:
            self.movement[1] = self.movement[1] + GRAVITY

        if self.is_jumping:
            self.index = 0
        elif self.is_blinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

        elif self.is_ducking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.is_dead:
            self.index = 4

        if not self.is_ducking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[self.index % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.check_bounds()

        if not self.is_dead and self.counter % 7 == 6 and self.is_blinking is False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() is not None:
                    if IS_SOUND_ENABLE:
                        CHECKPOINT_SOUND.play()

        self.counter = (self.counter + 1)


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, size_x=-1, size_y=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, size_x, size_y, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1 * speed, 0]

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=5, size_x=-1, size_y=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, size_x, size_y, -1)
        self.ptera_height = [height * 0.82, height * 0.75, height * 0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground:
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)
        APP_SCREEN.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90 * 30 / 42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1 * self.speed, 0]

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Scoreboard:
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.temp_images, self.temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self):
        APP_SCREEN.blit(self.image, self.rect)

    def update(self, score):
        score_digits = extract_digits(score)
        self.image.fill(BACKGROUND_COLOR)
        for s in score_digits:
            self.image.blit(self.temp_images[s], self.temp_rect)
            self.temp_rect.left += self.temp_rect.width
        self.temp_rect.left = 0


def intro_screen():
    temp_dino = Dino(1, 44, 47)
    temp_dino.is_blinking = True
    game_start = False

    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    logo, logo_rect = load_image('logo.png', 300, 140, -1)
    logo_rect.centerx = width * 0.6
    logo_rect.centery = height * 0.6
    while not game_start:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            return True
        else:
            for game_event in pygame.event.get():
                if game_event.type == pygame.QUIT:
                    return True
                if game_event.type == pygame.KEYDOWN:
                    if game_event.key == pygame.K_SPACE or game_event.key == pygame.K_UP:
                        temp_dino.is_jumping = True
                        temp_dino.is_blinking = False
                        temp_dino.movement[1] = -1 * temp_dino.jump_speed

        temp_dino.update()

        if pygame.display.get_surface() is not None:
            APP_SCREEN.fill(BACKGROUND_COLOR)
            APP_SCREEN.blit(temp_ground[0], temp_ground_rect)
            if temp_dino.is_blinking:
                APP_SCREEN.blit(logo, logo_rect)
            temp_dino.draw()

            pygame.display.update()

        CLOCK.tick(FPS)
        if temp_dino.is_jumping is False and temp_dino.is_blinking is False:
            game_start = True


class Game:
    def __init__(self, number_of_dino):
        global NB_ITERATION
        NB_ITERATION += 1
        self.game_speed = 4
        self.start_menu = False
        self.game_over = False
        self.game_quit = False
        self.number_of_dino = number_of_dino
        self.new_ground = Ground(-1 * self.game_speed)
        self.scb = Scoreboard()
        self.high_score = Scoreboard(width * 0.78)
        self.nb_dino_board = Scoreboard(width * 0.5)
        self.nb_iteration_board = Scoreboard(width * 0.3)
        self.counter = 0
        self.dinos = [Dino(i, 44, 47) for i in range(number_of_dino)]
        self.cacti = pygame.sprite.Group()
        self.pteras = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.last_obstacle = pygame.sprite.Group()
        self.saved_scores = {}

        Cactus.containers = self.cacti
        Ptera.containers = self.pteras
        Cloud.containers = self.clouds

        self.retry_button_image, self.retry_button_rect = load_image('replay_button.png', 35, 31, -1)
        self.game_over_image, self.game_over_rect = load_image('game_over.png', 190, 11, -1)

        self.temp_images, self.temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.HI_image = pygame.Surface((22, int(11 * 6 / 5)))
        self.HI_rect = self.HI_image.get_rect()
        self.HI_image.fill(BACKGROUND_COLOR)
        self.HI_image.blit(self.temp_images[10], self.temp_rect)
        self.temp_rect.left += self.temp_rect.width
        self.HI_image.blit(self.temp_images[11], self.temp_rect)
        self.HI_rect.top = height * 0.1
        self.HI_rect.left = width * 0.73

    def game_loop(self):
        while not self.game_quit:
            while self.start_menu:
                pass
            while not self.game_over:
                if pygame.display.get_surface() is None:
                    print("Couldn't load display surface")
                    self.game_quit = True
                    self.game_over = True
                else:
                    self.key_event_loop()

                self.dinos_loop()
                self.cactis_loop()
                # self.pteras_loop()
                self.clouds_loop()
                self.update_everything()
                self.ground_loop()
                CLOCK.tick(FPS)

                if self.counter % 700 == 699:
                    self.new_ground.speed -= 1
                    self.game_speed += 1

                self.counter = (self.counter + 1)

            if self.game_quit:
                break

            self.game_over_loop()

        pygame.quit()
        quit()

    def key_event_loop(self):
        for game_event in pygame.event.get():
            if game_event.type == pygame.QUIT:
                self.game_quit = True
                self.game_over = True

            if game_event.type == pygame.KEYDOWN:
                if game_event.key == pygame.K_SPACE:
                    self.jump(0)

                if game_event.key == pygame.K_DOWN:
                    self.duck(0)

            if game_event.type == pygame.KEYUP:
                if game_event.key == pygame.K_DOWN:
                    self.stop_duck(0)

    def dinos_loop(self):
        global HIGH_SCORE
        for dino in self.dinos:
            if dino.is_dead:
                self.dinos.remove(dino)
                self.saved_scores[dino.dino_id] = dino.score
                if dino.score > HIGH_SCORE:
                    HIGH_SCORE = dino.score
                if len(self.dinos) == 0:
                    self.game_over = True

    def cactis_loop(self):
        for c in self.cacti:
            c.movement[0] = -1 * self.game_speed
            for dino in self.dinos:
                if pygame.sprite.collide_mask(dino, c):
                    dino.is_dead = True
                    if pygame.mixer.get_init() is not None:
                        if IS_SOUND_ENABLE:
                            DIE_SOUND.play()

        if len(self.cacti) < 2:
            if len(self.cacti) == 0:
                cactus_size = random.randrange(35, 50)
                self.last_obstacle.empty()
                self.last_obstacle.add(Cactus(self.game_speed, cactus_size, cactus_size))
            else:
                for l in self.last_obstacle:
                    if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                        cactus_size = random.randrange(35, 50)
                        self.last_obstacle.empty()
                        self.last_obstacle.add(Cactus(self.game_speed, cactus_size, cactus_size))

    def pteras_loop(self):
        for p in self.pteras:
            p.movement[0] = -1 * self.game_speed
            for dino in self.dinos:
                if pygame.sprite.collide_mask(dino, p):
                    dino.is_dead = True
                    if pygame.mixer.get_init() is not None:
                        if IS_SOUND_ENABLE:
                            DIE_SOUND.play()

        if len(self.pteras) == 0 and random.randrange(0, 200) == 10 and self.counter > 500:
            for l in self.last_obstacle:
                if l.rect.right < width * 0.8:
                    self.last_obstacle.empty()
                    self.last_obstacle.add(Ptera(self.game_speed, 46, 40))

    def clouds_loop(self):
        if len(self.clouds) < 5 and random.randrange(0, 300) == 10:
            Cloud(width, random.randrange(height / 5, height / 2))

    def ground_loop(self):
        if pygame.display.get_surface() is not None:
            APP_SCREEN.fill(BACKGROUND_COLOR)
            self.new_ground.draw()
            self.clouds.draw(APP_SCREEN)
            self.scb.draw()
            self.nb_dino_board.draw()
            self.nb_iteration_board.draw()
            if HIGH_SCORE != 0:
                self.high_score.draw()
                APP_SCREEN.blit(self.HI_image, self.HI_rect)
            self.cacti.draw(APP_SCREEN)
            self.pteras.draw(APP_SCREEN)
            for dino in self.dinos:
                dino.draw()
            pygame.display.update()

    def game_over_loop(self):
        while self.game_over:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                self.game_quit = True
                self.game_over = False
            else:
                for game_event in pygame.event.get():
                    if game_event.type == pygame.QUIT:
                        self.game_quit = True
                        self.game_over = False
                    if game_event.type == pygame.KEYDOWN:
                        if game_event.key == pygame.K_ESCAPE:
                            self.game_quit = True
                            self.game_over = False

                        if game_event.key == pygame.K_RETURN or game_event.key == pygame.K_SPACE:
                            self.restart_game(self.number_of_dino)
            self.high_score.update(HIGH_SCORE)
            if pygame.display.get_surface() is not None:
                display_game_over_msg(self.retry_button_image, self.game_over_image)
                if HIGH_SCORE != 0:
                    self.high_score.draw()
                    APP_SCREEN.blit(self.HI_image, self.HI_rect)
                pygame.display.update()
            CLOCK.tick(FPS)

    def update_everything(self):
        for dino in self.dinos:
            dino.update()
        self.cacti.update()
        self.pteras.update()
        self.clouds.update()
        self.new_ground.update()
        if len(self.dinos) > 0:
            self.scb.update(self.dinos[0].score)
        self.high_score.update(HIGH_SCORE)
        self.nb_dino_board.update(len(self.dinos))
        self.nb_iteration_board.update(NB_ITERATION)

    def get_dino_with_id(self, dino_id):
        try:
            return list(filter(lambda dino: dino.dino_id == dino_id, self.dinos))[0]
        except IndexError:
            return None

    def jump(self, dino_id):
        dino = self.get_dino_with_id(dino_id)
        if dino is None:
            return
        if dino.rect.bottom == int(0.98 * height):
            dino.is_jumping = True
            if pygame.mixer.get_init() is not None:
                dino.movement[1] = -1 * dino.jump_speed
                if IS_SOUND_ENABLE:
                    JUMP_SOUND.play()

    def duck(self, dino_id):
        dino = self.get_dino_with_id(dino_id)
        if dino is None:
            return
        if not (dino.is_jumping and dino.is_dead):
                dino.is_ducking = True

    def stop_duck(self, dino_id):
        dino = self.get_dino_with_id(dino_id)
        if dino is None:
            return
        dino.is_ducking = False

    def dino_is_dead(self, dino_id):
        return self.get_dino_with_id(dino_id) is None

    def restart_game(self, nb_dino):
        self.game_over = False
        self.__init__(nb_dino)

    def get_speed(self):
        return self.game_speed

    def get_high_score(self):
        return self.high_score

    def get_nb_iteration(self):
        return NB_ITERATION

    def is_ducking(self, dino_id):
        dino = self.get_dino_with_id(dino_id)
        if dino is None:
            return False
        return dino.is_ducking

    def get_distance_of_first_obstacle(self):
        try:
            if len(self.cacti) != 0 and self.cacti.sprites()[0].rect.left - self.dinos[0].rect.right >= 0:
                return self.cacti.sprites()[0].rect.left - self.dinos[0].rect.right
            elif len(self.cacti) > 1:
                return self.cacti.sprites()[1].rect.left
        except AttributeError:
            pass

        return width

    def get_distance_between_first_and_second_obstacle(self):
        try:
            if len(self.cacti) < 2:
                return width
            else:
                if self.cacti.sprites()[0].rect.left - self.dinos[0].rect.right <= 0:
                    return width
                else:
                    return self.cacti.sprites()[1].rect.left - self.cacti.sprites()[0].rect.right
        except AttributeError:
            pass
        return width

    def get_saved_scores(self):
        return self.saved_scores

    def game_is_over(self):
            return self.game_over

    def set_simulation_speed_multiplier(self, value):
        global FPS
        FPS = 60 * value

    def set_nb_iteration(self, nb_iteration):
        global NB_ITERATION
        NB_ITERATION = nb_iteration


def start_game():
    is_game_quit = intro_screen()
    if not is_game_quit:
        game = Game(1)
        game.game_loop()


if __name__ == "__main__":
    start_game()
