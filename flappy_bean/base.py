from pygame.image import load
from pygame.transform import scale
from .constants import SCREEN_WDTH


class Base:
    SPEED = 5

    WDTH = SCREEN_WDTH
    HGHT = 100
    SIZE = WDTH, HGHT
    PATH = 'flappy_bean/media/base.png'

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WDTH

        self.image = scale(load(self.PATH), self.SIZE)

    def move(self):
        self.x0 -= self.SPEED
        self.x1 -= self.SPEED

        if self.x0 + self.WDTH < 0:
            self.x0 = self.x1 + self.WDTH
        elif self.x1 + self.WDTH < 0:
            self.x1 = self.x0 + self.WDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x0, self.y))
        screen.blit(self.image, (self.x1, self.y))
