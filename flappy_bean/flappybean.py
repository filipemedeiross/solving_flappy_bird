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
    
    DIGITS_PATH = [f'flappy_bean/media/{i}.png' for i in range(10)]

    def __init__(self):
        pygame.init()

        # Screen is initialized with init_game method
        self.screen = None

        # Create an object to help update the grid
        self.clock = pygame.time.Clock()

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

        self.digits = [pygame.transform.scale(pygame.image.load(path), DIGITS_SIZE) for path in self.DIGITS_PATH]
        self.first_digit_rect  = self.digits[0].get_rect(topleft=(SCORE_LEFT, SCORE_TOP))
        self.second_digit_rect = self.digits[0].get_rect(topleft=(SCORE_LEFT + DIGITS_SIDE, SCORE_TOP))

        # Initializing game objects
        self.bean = Bean(BEAN_MSCW, BEAN_MSCH)

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

        while True:
            self.clock.tick(25)

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
        pass


'''
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.draw(tela)
    for cano in canos:
        cano.draw(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (SCREEN_WDTH - 10 - texto.get_width(), 10))
    chao.draw(tela)
    pygame.display.update()


def main():
    passaros = [Bean(230, 350)]
    chao = Base(730)
    canos = [Pipe(700)]
    tela = pygame.display.set_mode((SCREEN_WDTH, SCREEN_HGHT))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.jump()

        # mover as coisas
        for passaro in passaros:
            passaro.move()
        chao.move()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.collide(passaro):
                    passaros.pop(i)
                if not cano.passed and passaro.x > cano.x:
                    cano.passed = True
                    adicionar_cano = True
            cano.move()
            if cano.x + cano.pipe_top.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Pipe(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.image.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()
'''