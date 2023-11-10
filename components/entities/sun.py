from components.media import media
from components.entities import Entity
from random import randint

SUN_SIZE = 45

class Sun(Entity):
    def __init__(self, value=25, x_range: tuple[int, int] = (100, 980), y_range: tuple[int, int] = (200, 700)):
        self.value = value
        Entity.__init__(self, media.load_image('entities/sun.png', (SUN_SIZE, SUN_SIZE)))
        self.rect.center = (randint(*x_range), -SUN_SIZE)
        self.move_limit = SUN_SIZE / 2 + y_range[0] + randint(0, y_range[1])
        self.velocity_x = 5
