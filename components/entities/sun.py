import math
from pygame.transform import scale
from components.media import media
from components.entities import Entity
from utils.constants import FPS
import components.events as events
import utils.asynclib as asynclib

size = (80, 80)

class Sun(Entity):
    def __init__(self, value=25):
        self.value = value
        Entity.__init__(self, media.load_image('entities/sun.png', size))
        self.velocity_y = 3
        # self.velocity_a = 1 * (1 if randint(0, 1) else -1)
        self.z_index = 999
        self.radius_scale = 1
        self.cursor_r = 'hand'
        self.add_event_listener(events.CLICK_R, lambda: self.kill())
        self.autopick_taskid = asynclib.set_timeout(lambda: self.kill() if self.scene is not None else None, 5000)

    def kill(self):
        '''Returns sun value.'''
        controller.level.add_suns(self.value)
        asynclib.clear_timeout(self.autopick_taskid)
        if controller.level.victory is not None:
            Entity.kill(self)
            return self.value
        end_pos = controller.level.card_board_sun_icon.rect.center
        t = 0
        duration = 0.25 * FPS
        self.velocity_x = (end_pos[0] - self.rect.centerx) / duration
        self.velocity_y = (end_pos[1] - self.rect.centery) / duration
        self.move_limit = math.dist(end_pos, self.rect.center)
        self.image_0 = self.image
        def _update():
            nonlocal t
            t += 1
            self.image = scale(self.image_0, (size[0] * (1 - (0.5 * t / duration)), size[1] * (1 - (0.5 * t / duration))))
            if self.move_limit <= 0:
                Entity.kill(self)
        self.update = _update
        self.kill = lambda: None
        return self.value

from components import controller