import csv
import random
import pickle
import webbrowser

import pygame
from .bean import Bean
from .pipe import Pipe
from .base import Base
from .constants import *


class FlappyBean:
    def __init__(self, data_path):
        pygame.init()

        # Creating the screen, clock and mixer
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Flappy Bean')

        self.clock = pygame.time.Clock()

        self.music_game = pygame.mixer.Sound(GAME_THEME_PATH)
        self.music_lose = pygame.mixer.Sound(GAME_EFFCT_PATH)
        self.channel_music = pygame.mixer.Channel(0)
        self.channel_effct = pygame.mixer.Channel(1)

        # Loading images used in the game
        self.bg = self.load_image(GAME_BG_PATH, SCREEN_SIZE)

        self.flappy = self.load_image(GAME_FLAPPY_PATH, FLAPPY_SIZE)
        self.flappy_rect = self.flappy.get_rect(midtop=(SCREEN_MIDW, FLAPPY_TOP))

        self.finger = self.load_image(GAME_FINGER_PATH, FINGER_SIZE)
        self.finger_rect = self.finger.get_rect(midtop=(SCREEN_MIDW, FINGER_TOP))

        self.tap_left  = self.load_image(GAME_TAPLEFT_PATH , TAP_SIZE)
        self.tap_right = self.load_image(GAME_TAPRIGHT_PATH, TAP_SIZE)
        self.tap_left_rect  = self.tap_left.get_rect(topright=(self.finger_rect.left  - SPACING, FINGER_TOP))
        self.tap_right_rect = self.tap_right.get_rect(topleft=(self.finger_rect.right + SPACING, FINGER_TOP))

        self.get_ready = self.load_image(GAME_GETREADY_PATH, GETREADY_SIZE)
        self.get_ready_rect = self.get_ready.get_rect(midtop=(SCREEN_MIDW, self.finger_rect.bottom + SPACING_3))

        self.share = self.load_image(GAME_SHARE_PATH, SHARE_SIZE)
        self.share_rect = self.share.get_rect(midtop=(SCREEN_MIDW, self.get_ready_rect.bottom + SPACING_2))

        self.game_over = self.load_image(GAME_GAMEOVER_PATH, GAMEOVER_SIZE)
        self.game_over_rect = self.game_over.get_rect(midtop=(SCREEN_MIDW, GAMEOVER_TOP))

        self.menu = self.load_image(GAME_MENU_PATH, MENU_SIZE)
        self.menu_rect = self.menu.get_rect(topleft=(self.game_over_rect.left, self.game_over_rect.bottom + SPACING))

        self.ok = self.load_image(GAME_OK_PATH, OK_SIZE)
        self.ok_rect = self.ok.get_rect(topright=(self.game_over_rect.right, self.game_over_rect.bottom + SPACING))

        self.digits = [self.load_image(path, DIGITS_SIZE) for path in GAME_DIGITS_PATH]
        self.first_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT                  , SCORE_TOP))
        self.second_digit_rect = self.digits[0].get_rect(topleft=(SCORE_LEFT +     DIGITS_SIDE, SCORE_TOP))
        self.third_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT + 2 * DIGITS_SIDE, SCORE_TOP))

        # Initializing game objects
        self.bean  = Bean()
        self.base  = Base(BASE_TOP)
        self.pipes = []

        self.load_agent()

        self.data_path = data_path
        if data_path:
            self.data = []

    def init_game(self):
        while True:
            self.main_screen()
            self.play()

    def main_screen(self):
        self.init_main_screen()
        self.display_main_screen()

        while True:
            self.clock.tick(FRAMERATE_MS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        return
                if event.type == MOUSEBUTTONDOWN:
                    if self.bean.get_rect.collidepoint(event.pos):
                        self.player = False
                        return
                    if self.finger_rect.collidepoint(event.pos):
                        return
                    if self.share_rect.collidepoint(event.pos):
                        webbrowser.open('https://github.com/filipemedeiross/', new=2)

            self.update_main_screen()
    
    def play(self):#
        self.init_play_screen()

        while True:
            self.clock.tick(FRAMERATE_PS)

            jumped = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                if self.lose:
                    if event.type == MOUSEBUTTONDOWN:
                        if self.menu_rect.collidepoint(event.pos):
                            return
                        if self.ok_rect.collidepoint(event.pos):
                            self.init_play_screen()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            self.init_play_screen()
                elif self.player:
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            jumped = True
                            self.bean.jump()

            if not self.lose:
                if not self.player:
                    if self.predict(self.capture_data()):
                        jumped = True
                        self.bean.jump()

                if self.data_path:
                    x, y = self.capture_data()
                    self.data.append([x, y, jumped])

                self.move_objects()

                pipe = self.pipes[0]
                if self.collide(self.bean, pipe, self.base):
                    self.lose = True
                    self.play_lose_effect()
                elif pipe.right < 0:
                    self.pipes.pop(0)
                elif not pipe.passed and self.bean.x > pipe.right:
                    self.score += 1
                    pipe.passed = True
                    self.pipes.append(Pipe(PIPE_NX))

                    if self.data_path:
                        self.save_data()

                self.display_play_screen()
                if self.lose:
                    self.display_lose_options()

                pygame.display.flip()

    def init_main_screen(self):
        self.bean.center = SCREEN_MIDD
        self.player = True

        self.play_theme()

    def display_main_screen(self):
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.flappy, self.flappy_rect)
        self.screen.blit(self.finger, self.finger_rect)
        self.screen.blit(self.tap_left, self.tap_left_rect)
        self.screen.blit(self.tap_right, self.tap_right_rect)
        self.screen.blit(self.get_ready, self.get_ready_rect)
        self.screen.blit(self.share, self.share_rect)

        pygame.display.flip()

    def update_main_screen(self):
        # Clearing current bean position
        self.screen.blit(self.bg,
                         self.bean.topleft,
                         area=self.bean.rect)
        pygame.display.update(self.bean.rect)

        # Moving the bean and drawing it
        if self.bean.y >= SCREEN_MIDH:
            self.bean.jump()

        self.bean.move()
        self.bean.draw(self.screen)

        pygame.display.update(self.bean.rect)

    def init_play_screen(self):#
        self.lose  = False
        self.score = 0
        if self.data_path:
            self.data.clear()

        self.bean.topleft = BEAN_PSCW, BEAN_PSCH
        self.pipes.clear()
        self.pipes.append(Pipe(PIPE_X))

        self.play_theme()

    def display_play_screen(self):#
        self.screen.blit(self.bg, (0, 0))

        self.bean.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.base.draw(self.screen)

        self.display_score()

    def display_score(self):#
        self.screen.blit(self.digits[self.score // 100], self.first_digit_rect)
        self.screen.blit(self.digits[self.score // 10 % 10], self.second_digit_rect)
        self.screen.blit(self.digits[self.score % 10], self.third_digit_rect)

    def display_lose_options(self):#
        self.screen.blit(self.game_over, self.game_over_rect)
        self.screen.blit(self.menu, self.menu_rect)
        self.screen.blit(self.ok, self.ok_rect)

    def move_objects(self):#
        self.bean.move()
        self.base.move()
        for pipe in self.pipes:
            pipe.move()

    @staticmethod
    def collide(bean, pipe, base):
        return pipe.collide(bean)    or \
               base.y <= bean.bottom or \
               bean.y <= 0

    def play_theme(self):
        if not self.channel_music.get_busy():
            self.channel_music.play(self.music_game, -1)

    def play_lose_effect(self):
        self.channel_music.stop()
        self.channel_effct.play(self.music_lose)

    def capture_data(self):
        for pipe in self.pipes:
            if self.bean.x <= pipe.right:
                return pipe.centerx - self.bean.centerx, \
                       pipe.centery - self.bean.centery

    def save_data(self):
        with open(self.data_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

        self.data.clear()

    def load_agent(self):
        path = random.choice([LOGISTIC_REGR_PATH,
                              DECISION_TREE_PATH,
                              SVM_RBF_PATH])

        with open(path, 'rb') as f:
            self.agent = pickle.load(f)

    def predict(self, xy):
        return self.agent.predict([xy])

    @staticmethod
    def load_image(path, size):
        return pygame.transform.scale(pygame.image.load(path), size)
