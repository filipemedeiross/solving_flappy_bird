import pygame
from .bean import Bean
from .pipe import Pipe
from .base import Base
from .constants import *
from webbrowser import open


class FlappyBean:
    BG_PATH = 'flappy_bean/media/bg.png'

    FLAPPY_PATH   = 'flappy_bean/media/flappy.png'
    FINGER_PATH   = 'flappy_bean/media/finger.png'
    TAPLEFT_PATH  = 'flappy_bean/media/tap_left.png'
    TAPRIGHT_PATH = 'flappy_bean/media/tap_right.png'
    GETREADY_PATH = 'flappy_bean/media/get_ready.png'
    SHARE_PATH    = 'flappy_bean/media/share.png'

    GAMEOVER_PATH = 'flappy_bean/media/game_over.png'
    MENU_PATH     = 'flappy_bean/media/menu.png'
    OK_PATH       = 'flappy_bean/media/ok.png'
    DIGITS_PATH = [f'flappy_bean/media/{i}.png' for i in range(10)]

    THEME_PATH = 'flappy_bean/media/epic_at_the_jungle.mp3'
    EFFCT_PATH = 'flappy_bean/media/gameover.mp3'
    def __init__(self):
        pygame.init()

        # Screen is initialized with init_game method
        self.screen = None

        # Init the clock
        self.clock = pygame.time.Clock()
        
        # Init the mixer
        self.music_game = pygame.mixer.Sound(self.THEME_PATH)
        self.music_lose = pygame.mixer.Sound(self.EFFCT_PATH)

        self.channel_music = pygame.mixer.Channel(0)
        self.channel_effct = pygame.mixer.Channel(1)

        self.music_game.set_volume(0.5)

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
        self.get_ready_rect = self.get_ready.get_rect(midtop=(SCREEN_MIDW, self.finger_rect.bottom + 3 * SPACING))

        self.share = pygame.transform.scale(pygame.image.load(self.SHARE_PATH), SHARE_SIZE)
        self.share_rect = self.share.get_rect(midtop=(SCREEN_MIDW, self.get_ready_rect.bottom + 2 * SPACING))

        self.game_over = pygame.transform.scale(pygame.image.load(self.GAMEOVER_PATH), GAMEOVER_SIZE)
        self.game_over_rect = self.game_over.get_rect(center=(SCREEN_MIDW, GAMEOVER_TOP))

        self.menu = pygame.transform.scale(pygame.image.load(self.MENU_PATH), MENU_SIZE)
        self.menu_rect = self.menu.get_rect(topleft=(self.game_over_rect.left, self.game_over_rect.bottom + SPACING))

        self.ok = pygame.transform.scale(pygame.image.load(self.OK_PATH), OK_SIZE)
        self.ok_rect = self.ok.get_rect(topright=(self.game_over_rect.right, self.game_over_rect.bottom + SPACING))

        self.digits = [pygame.transform.scale(pygame.image.load(path), DIGITS_SIZE) for path in self.DIGITS_PATH]
        self.first_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT, SCORE_TOP))
        self.second_digit_rect = self.digits[0].get_rect(topleft=(SCORE_LEFT + DIGITS_SIDE, SCORE_TOP))
        self.third_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT + 2 * DIGITS_SIDE, SCORE_TOP))

        # Initializing game objects
        self.bean  = Bean(0, 0)
        self.pipes = []
        self.base  = Base(BASE_Y)

    # Method that start the game
    def init_game(self):
        # Creating a display Surface
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Flappy Bean')

        while True:
            self.main_screen()
            self.play()

    def main_screen(self):
        # Preparing the main screen
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.flappy, self.flappy_rect)
        self.screen.blit(self.finger, self.finger_rect)
        self.screen.blit(self.tap_left, self.tap_left_rect)
        self.screen.blit(self.tap_right, self.tap_right_rect)
        self.screen.blit(self.get_ready, self.get_ready_rect)
        self.screen.blit(self.share, self.share_rect)

        pygame.display.flip()  # displaying the screen

        self.bean.topleft = BEAN_MSCW, BEAN_MSCH

        if not self.channel_music.get_busy():
            self.channel_music.play(self.music_game, -1)

        while True:
            self.clock.tick(FRAMERATE_MS)

            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)  # leaving the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.finger_rect.collidepoint(event.pos):
                        return
                    if self.share_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

            self.screen.blit(self.background,
                             self.bean.topleft,
                             area=self.bean.rect)
            pygame.display.update(self.bean.rect)
            
            self.bean.move()
            if self.bean.y >= SCREEN_MIDH:
                self.bean.jump()

            self.bean.draw(self.screen)
            pygame.display.update(self.bean.rect)
    
    def play(self):
        lose, score = self.init_variables()

        while True:
            self.clock.tick(FRAMERATE_PS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if lose:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu_rect.collidepoint(event.pos):
                            return
                        if self.ok_rect.collidepoint(event.pos):
                            lose, score = self.init_variables()
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bean.jump()

            if not lose:
                self.bean.move()
                self.base.move()
                for pipe in self.pipes:
                    pipe.move()

                pipe = self.pipes[0]
                if pipe.collide(self.bean):
                    lose = True

                    self.channel_music.stop()
                    self.channel_effct.play(self.music_lose)
                elif not pipe.passed and self.bean.x > pipe.x:
                    score += 1
                    pipe.passed = True
                    self.pipes.append(Pipe(PIPE_NX))
                elif pipe.x + pipe.pipe_top.get_width() < 0:
                    self.pipes.pop(0)

                if self.bean.bottomright[1] > self.base.y or self.bean.y < 0:
                    lose = True

                    self.channel_music.stop()
                    self.channel_effct.play(self.music_lose)
                self.screen.blit(self.background, (0, 0))

                self.bean.draw(self.screen)
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.base.draw(self.screen)

                self.screen.blit(self.digits[score // 100], self.first_digit_rect)
                self.screen.blit(self.digits[score // 10], self.second_digit_rect)
                self.screen.blit(self.digits[score % 10], self.third_digit_rect)

                if lose:
                    self.screen.blit(self.game_over, self.game_over_rect)
                    self.screen.blit(self.menu, self.menu_rect)
                    self.screen.blit(self.ok, self.ok_rect)

                pygame.display.flip()

    def init_variables(self):
        if not self.channel_music.get_busy():
            self.channel_music.play(self.music_game, -1)

        self.bean.topleft = BEAN_PSCW, BEAN_PSCH
        self.pipes.clear()
        self.pipes.append(Pipe(PIPE_X))

        return False, 0
