from pygame.image import load
from pygame.transform import scale
from .constants import BASE_PATH, \
                       BASE_WDTH, \
                       BASE_HGHT, \
                       SPEED_ANIMATION


class Base:
    SPEED = SPEED_ANIMATION

    WDTH  = BASE_WDTH
    HGHT  = BASE_HGHT
    SIZE  = WDTH, HGHT
    PATH  = BASE_PATH

    def __init__(self, y):
        self.x = 0
        self.y = y

        self.image = self.load_image(self.PATH, self.SIZE)

    def move(self):
        self.x -= self.SPEED

        if self.x + self.width < 0:
            self.x += self.width

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.image, (self.x + self.width, self.y))

    @property
    def width(self):
        return self.WDTH

    @property
    def height(self):
        return self.HGHT

    @staticmethod
    def load_image(path, size):
        return scale(load(path), size)
