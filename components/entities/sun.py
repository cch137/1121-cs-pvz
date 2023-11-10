from components.media import media
from components.entities import Entity
from random import randint

class Sun(Entity):
    def __init__(self, value=25, x_range: tuple[int, int] = (100, 980), y_range: tuple[int, int] = (200, 700)):
        self.value = value
        Entity.__init__(self, media.load_image('entities/sun.png', 75))
        self.rect.center = (randint(*x_range), -self.rect.height / 2)
        self.move_limit = int(self.rect.height / 2 + randint(*y_range))
        self.velocity_y = 3
        self.velocity_a = 1 * (1 if randint(0, 1) else -1)
        self.z_index = 999
        self.cursor = 'hand'
    
    def update(self):
        if self.move_limit <= 0:
            self.velocity_a = 0
    
    def kill(self, *args, **kwargs):
        '''Returns sun value.'''
        Entity.kill(self, *args, **kwargs)
        return self.value
