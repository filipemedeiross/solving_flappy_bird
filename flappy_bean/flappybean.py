import pygame
from .bean import Bean
from .pipe import Pipe
from .base import Base
from .constants import *
from webbrowser import open


class FlappyBean:
    BG_PATH       = GAME_BG_PATH
    FLAPPY_PATH   = GAME_FLAPPY_PATH
    FINGER_PATH   = GAME_FINGER_PATH
    TAPLEFT_PATH  = GAME_TAPLEFT_PATH
    TAPRIGHT_PATH = GAME_TAPRIGHT_PATH
    GETREADY_PATH = GAME_GETREADY_PATH
    SHARE_PATH    = GAME_SHARE_PATH
    GAMEOVER_PATH = GAME_GAMEOVER_PATH
    MENU_PATH     = GAME_MENU_PATH
    OK_PATH       = GAME_OK_PATH
    DIGITS_PATH   = GAME_DIGITS_PATH
    THEME_PATH    = GAME_THEME_PATH
    EFFCT_PATH    = GAME_EFFCT_PATH

    def __init__(self):
        pygame.init()

        # Screen is initialized with init_game method
        self.screen = None

        # Init the clock and mixer
        self.clock = pygame.time.Clock()
        
        self.music_game = pygame.mixer.Sound(self.THEME_PATH)
        self.music_lose = pygame.mixer.Sound(self.EFFCT_PATH)

        self.channel_music = pygame.mixer.Channel(0)
        self.channel_effct = pygame.mixer.Channel(1)

        # Loading images used in the game
        self.background = pygame.transform.scale(pygame.image.load(self.BG_PATH), SCREEN_SIZE)

        self.flappy = pygame.transform.scale(pygame.image.load(self.FLAPPY_PATH), FLAPPY_SIZE)
        self.flappy_rect = self.flappy.get_rect(midtop=(SCREEN_MIDW, FLAPPY_TOP))

        self.finger = pygame.transform.scale(pygame.image.load(self.FINGER_PATH), FINGER_SIZE)
        self.finger_rect = self.finger.get_rect(midtop=(SCREEN_MIDW, FINGER_TOP))

        self.tap_left  = pygame.transform.scale(pygame.image.load(self.TAPLEFT_PATH), TAP_SIZE)
        self.tap_right = pygame.transform.scale(pygame.image.load(self.TAPRIGHT_PATH), TAP_SIZE)
        self.tap_left_rect  = self.tap_left.get_rect(topright=(self.finger_rect.left - SPACING, FINGER_TOP))
        self.tap_right_rect = self.tap_right.get_rect(topleft=(self.finger_rect.right + SPACING, FINGER_TOP))

        self.get_ready = pygame.transform.scale(pygame.image.load(self.GETREADY_PATH), GETREADY_SIZE)
        self.get_ready_rect = self.get_ready.get_rect(midtop=(SCREEN_MIDW, self.finger_rect.bottom + SPACING_3))

        self.share = pygame.transform.scale(pygame.image.load(self.SHARE_PATH), SHARE_SIZE)
        self.share_rect = self.share.get_rect(midtop=(SCREEN_MIDW, self.get_ready_rect.bottom + SPACING_2))

        self.game_over = pygame.transform.scale(pygame.image.load(self.GAMEOVER_PATH), GAMEOVER_SIZE)
        self.game_over_rect = self.game_over.get_rect(midtop=(SCREEN_MIDW, GAMEOVER_TOP))

        self.menu = pygame.transform.scale(pygame.image.load(self.MENU_PATH), MENU_SIZE)
        self.menu_rect = self.menu.get_rect(topleft=(self.game_over_rect.left, self.game_over_rect.bottom + SPACING))

        self.ok = pygame.transform.scale(pygame.image.load(self.OK_PATH), OK_SIZE)
        self.ok_rect = self.ok.get_rect(topright=(self.game_over_rect.right, self.game_over_rect.bottom + SPACING))

        self.digits = [pygame.transform.scale(pygame.image.load(p), DIGITS_SIZE) for p in self.DIGITS_PATH]
        self.first_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT, SCORE_TOP))
        self.second_digit_rect = self.digits[0].get_rect(topleft=(SCORE_LEFT + DIGITS_SIDE, SCORE_TOP))
        self.third_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT + 2 * DIGITS_SIDE, SCORE_TOP))

        # Initializing game objects
        self.lose  = None
        self.score = None

        self.bean  = Bean(BEAN_MSCW, BEAN_MSCH)
        self.base  = Base(SCREEN_HGHT - BASE_HGHT)
        self.pipes = []

    def init_game(self):
        # Creating a display Surface
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Flappy Bean')

        while True:
            self.main_screen()
            self.play()

    def main_screen(self):
        self.init_main_screen()
        self.display_main_screen()

        while True:
            self.clock.tick(FRAMERATE_MS)

            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)  # leaving the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.finger_rect.collidepoint(event.pos):
                        return
                    if self.share_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

            self.update_main_screen()
    
    def play(self):
        self.init_play_screen()

        while True:
            self.clock.tick(FRAMERATE_PS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if self.lose:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu_rect.collidepoint(event.pos):
                            return
                        if self.ok_rect.collidepoint(event.pos):
                            self.init_play_screen()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bean.jump()

            if not self.lose:
                self.move_objects()

                pipe = self.pipes[0]
                if self.collide(self.bean, pipe, self.base):
                    self.lose = True
                    self.play_lose_effect()
                elif not pipe.passed and self.bean.x > pipe.x:
                    self.score += 1
                    pipe.passed = True
                    self.pipes.append(Pipe(PIPE_NX))
                elif pipe.x + pipe.pipe_top.get_width() < 0:
                    self.pipes.pop(0)

                self.display_play_screen()
                if self.lose:
                    self.display_lose_options()

                pygame.display.flip()

    def init_main_screen(self):
        self.bean.topleft = BEAN_MSCW, BEAN_MSCH

        self.play_theme()
    
    def display_main_screen(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.flappy, self.flappy_rect)
        self.screen.blit(self.finger, self.finger_rect)
        self.screen.blit(self.tap_left, self.tap_left_rect)
        self.screen.blit(self.tap_right, self.tap_right_rect)
        self.screen.blit(self.get_ready, self.get_ready_rect)
        self.screen.blit(self.share, self.share_rect)

        pygame.display.flip()

    def update_main_screen(self):
        # Clearing current bean position
        self.screen.blit(self.background,
                         self.bean.topleft,
                         area=self.bean.rect)
        pygame.display.update(self.bean.rect)
        
        # Moving the bean
        if self.bean.y >= SCREEN_MIDH:
            self.bean.jump()
        self.bean.move()

        # Drawing the bean in the new position
        self.bean.draw(self.screen)
        pygame.display.update(self.bean.rect)

    def init_play_screen(self):
        self.lose  = False
        self.score = 0

        self.bean.topleft = BEAN_PSCW, BEAN_PSCH
        self.pipes.clear()
        self.pipes.append(Pipe(PIPE_X))

        self.play_theme()

    def display_play_screen(self):
        self.screen.blit(self.background, (0, 0))

        self.bean.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.base.draw(self.screen)

        self.display_score()

    def display_score(self):
        self.screen.blit(self.digits[self.score // 100], self.first_digit_rect)
        self.screen.blit(self.digits[self.score // 10], self.second_digit_rect)
        self.screen.blit(self.digits[self.score % 10], self.third_digit_rect)

    def display_lose_options(self):
        self.screen.blit(self.game_over, self.game_over_rect)
        self.screen.blit(self.menu, self.menu_rect)
        self.screen.blit(self.ok, self.ok_rect)

    def move_objects(self):
        self.bean.move()
        self.base.move()
        for pipe in self.pipes:
            pipe.move()
    
    def play_theme(self):
        if not self.channel_music.get_busy():
            self.channel_music.play(self.music_game, -1)

    def play_lose_effect(self):
        self.channel_music.stop()
        self.channel_effct.play(self.music_lose)

    @staticmethod
    def collide(bean, pipe, base):
        return pipe.collide(bean) or \
               bean.bottomright[1] > base.y or \
               bean.y < 0
