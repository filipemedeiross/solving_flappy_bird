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
             'flappy_bean/media/bean4.png']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.images = self.load_images()
        self.n_images = len(self.images)

        self.jump()

    def load_images(self):
        return [scale(load(path), self.SIZE)
                for path in self.PATHS]

    def jump(self):
        self.index = 0
        self.image = self.images[self.index]

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
            self.image = self.images[1]
        else:
            self.index += 1
            self.image = self.images[self.index // self.TIME_ANIMATION % self.n_images]

        rotated_image = rotate(self.image, self.angle)
        screen.blit(rotated_image, (self.x, self.y))

    def get_mask(self):
        return from_surface(self.image)
