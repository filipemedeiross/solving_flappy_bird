from pygame.image import load
from pygame.transform import scale, rotate
from pygame.mask import from_surface
from .constants import BEAN_SPEED, BEAN_ACCELERATION, BEAN_MAX_DELTA, \
                       BEAN_MAX_ROTATION, BEAN_FLY_ROTATION, BEAN_MIN_ROTATION, \
                       BEAN_SPD_ROTATION, SPEED_ANIMATION, \
                       BEAN_WDTH, BEAN_HGHT, BEAN_PATHS


class Bean:
    SPEED = BEAN_SPEED
    ACCELERATION = BEAN_ACCELERATION
    MAX_DELTA = BEAN_MAX_DELTA

    SPD_ROTATION = BEAN_SPD_ROTATION
    MAX_ROTATION = BEAN_MAX_ROTATION
    FLY_ROTATION = BEAN_FLY_ROTATION
    MIN_ROTATION = BEAN_MIN_ROTATION
    TIME_ANIMATION = SPEED_ANIMATION

    WDTH = BEAN_WDTH
    HGHT = BEAN_HGHT
    SIZE = WDTH, HGHT
    PATHS = BEAN_PATHS
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.imgs = self.load_images()
        self.n_imgs = len(self.imgs)

        self.jump()

    def load_images(self):
        return [scale(load(p), self.SIZE) for p in self.PATHS]

    def jump(self):
        self.idx = 0
        self.img = self.imgs[self.idx]

        self.time = 0
        self.angle = self.MAX_ROTATION
        self.height = self.y

    def move(self):
        self.time += 1

        delta = self.SPEED * self.time + self.ACCELERATION * self.time**2
        if delta > self.MAX_DELTA:
            delta = self.MAX_DELTA

        self.y += delta

        if delta > 0 and self.y > self.height and self.angle > self.MIN_ROTATION:
            self.angle -= self.SPD_ROTATION

    def draw(self, screen):
        if self.angle <= self.FLY_ROTATION:
            self.img = self.imgs[1]
        else:
            self.idx += 1
            self.img = self.imgs[self.idx // self.TIME_ANIMATION % self.n_imgs]
        
        self.img = rotate(self.img, self.angle)
        screen.blit(self.img, (self.x, self.y))

    @property
    def topleft(self):
        return self.x, self.y
    
    @topleft.setter
    def topleft(self, topleft):
        self.x = topleft[0]
        self.y = topleft[1]

    @property
    def center(self):
        return self.x + (self.img.get_width() / 2), self.y + (self.img.get_height() / 2)

    @property
    def bottomright(self):
        return self.x + self.img.get_width(), self.y + self.img.get_height()
    
    @property
    def rect(self):
        return self.x, self.y, self.img.get_width(), self.img.get_height()
    
    @property
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))

    @property
    def mask(self):
        return from_surface(self.img)
