from pygame.image import load
from pygame.transform import scale, rotate
from pygame.mask import from_surface


class Bean:
    SPEED = -10.5
    ACCELERATION = 1.5
    MAX_DELTA = 16

    SPD_ROTATION = 15
    MAX_ROTATION = 30
    FLY_ROTATION = -70
    MIN_ROTATION = -90
    TIME_ANIMATION = 5

    WDTH = 50
    HGHT = 40
    SIZE = WDTH, HGHT
    PATHS = ['flappy_bean/media/bean1.png',
             'flappy_bean/media/bean2.png',
             'flappy_bean/media/bean3.png',
             'flappy_bean/media/bean2.png']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.imgs = self.load_images()
        self.n_imgs = len(self.imgs)

        self.jump()

    def load_images(self):
        return [scale(load(path), self.SIZE)
                for path in self.PATHS]

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
    
    @property
    def rect(self):
        return self.x, self.y, self.img.get_width(), self.img.get_height()

    @property
    def mask(self):
        return from_surface(self.img)
