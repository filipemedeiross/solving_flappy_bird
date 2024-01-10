from pygame.image import load
from pygame.transform import scale
from .constants import SPEED_ANIMATION, BASE_WDTH, BASE_HGHT, BASE_PATH


class Base:
    SPEED = SPEED_ANIMATION
    WDTH  = BASE_WDTH
    HGHT  = BASE_HGHT
    PATH  = BASE_PATH

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.WDTH

        self.image = scale(load(self.PATH), (self.WDTH, self.HGHT))

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

    @property
    def width(self):
        return self.WDTH
    
    @property
    def height(self):
        return self.HGHT
