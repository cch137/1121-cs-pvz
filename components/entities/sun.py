from components.media import media
from components.entities import Entity
from random import randint

class Sun(Entity):
    def __init__(self, value=25, x_range: tuple[int, int] = (100, 980), y_range: tuple[int, int] = (200, 700)):
        self.value = value
        Entity.__init__(self, media.load_image('entities/sun.png', (75, 75)))
        self.rect.center = (randint(*x_range), -60)
        self.move_limit = int(60 / 2 + randint(*y_range))
        self.velocity_y = 3
        self.z_index = 999
        self.cursor = 'hand'
    
    def kill(self, *args, **kwargs):
        '''Returns sun value.'''
        Entity.kill(self, *args, **kwargs)
        return self.value
