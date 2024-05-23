from pygame.image import load
from pygame.transform import scale, rotate
from pygame.mask import from_surface
from .constants import BEAN_SPEED, BEAN_ACCELERATION, TIME_ANIMATION,           \
                       BEAN_SPD_ROTATION, BEAN_MAX_TIME, BEAN_MAX_DELTA,        \
                       BEAN_FLY_ROTATION, BEAN_MIN_ROTATION, BEAN_MAX_ROTATION, \
                       BEAN_WDTH, BEAN_HGHT, BEAN_PATHS


class Bean:
    SPEED = BEAN_SPEED
    ACCEL = BEAN_ACCELERATION
    MAX_TIME  = BEAN_MAX_TIME
    MAX_DELTA = BEAN_MAX_DELTA

    SPD_ROTATION = BEAN_SPD_ROTATION
    MAX_ROTATION = BEAN_MAX_ROTATION
    MIN_ROTATION = BEAN_MIN_ROTATION
    FLY_ROTATION = BEAN_FLY_ROTATION
    TIME_ANIMATION = TIME_ANIMATION

    WDTH = BEAN_WDTH
    HGHT = BEAN_HGHT
    SIZE = WDTH, HGHT
    PATHS = BEAN_PATHS

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.load_images()
        self.jump()

    def jump(self):
        self.idx = 0
        self.img = self.imgs[self.idx]

        self.time   = 0
        self.angle  = self.MAX_ROTATION
        self.angley = self.y

    def move(self):
        if self.time > self.MAX_TIME:
            delta = self.MAX_DELTA
        else:
            self.time += 1
            delta = self.SPEED * self.time +  \
                    self.ACCEL * self.time**2

        self.y += delta
        if self.rotational(delta):
            self.angle -= self.SPD_ROTATION

    def draw(self, surface):
        if self.angle <= self.MIN_ROTATION:
            self.img = self.imgs[-1]
        else:
            self.img = self.imgs[1]                       \
                       if self.angle <= self.FLY_ROTATION \
                       else self.imgs[self.id_img]
            self.img = rotate(self.img, self.angle)

        surface.blit(self.img, self.topleft)

    def rotational(self, delta):
        return delta      > 0           and \
               self.y     > self.angley and \
               self.angle > self.MIN_ROTATION

    def load_images(self):
        self.imgs = [self.load_image(path, self.SIZE)
                     for path in self.PATHS]
        self.n_imgs = len(self.imgs)

        self.imgs.append(rotate(self.imgs[1], self.MIN_ROTATION))

    @property
    def rect(self):
        return self.x, self.y, self.width, self.height

    @property
    def get_rect(self):
        return self.img.get_rect(topleft=self.topleft)

    @property
    def mask(self):
        return from_surface(self.img)

    @property
    def topleft(self):
        return self.x, self.y

    @topleft.setter
    def topleft(self, topleft):
        self.x, self.y = topleft

    @property
    def centerx(self):
        return self.x + self.width / 2

    @property
    def centery(self):
        return self.y + self.height / 2

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def width(self):
        return self.img.get_width()

    @property
    def height(self):
        return self.img.get_height()

    @property
    def id_img(self):
        self.idx += 1

        return self.idx // self.TIME_ANIMATION % self.n_imgs

    @staticmethod
    def load_image(path, size):
        return scale(load(path), size)
