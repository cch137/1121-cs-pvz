from components.media import media
from components.entities import Entity
from random import randint
from typing import Tuple, Any
import components.events as events

class Sun(Entity):
    def __init__(self, value=25):
        self.value = value
        Entity.__init__(self, media.load_image('entities/sun.png', 80))
        self.velocity_y = 3
        # self.velocity_a = 1 * (1 if randint(0, 1) else -1)
        self.z_index = 999
        self.radius_scale = 0.7
        self.cursor_r = 'hand'
        self.add_event_listener(events.CLICK_R, lambda: controller.level.add_suns(self.kill()))

    def kill(self, *args: Any, **kwargs: Any):
        '''Returns sun value.'''
        Entity.kill(self, *args, **kwargs)
        return self.value

from components import controller