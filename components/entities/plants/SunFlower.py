from utils.constants import *
from components.entities.plants import Plant
from components.media import media
from components.entities.Sun import Sun
from random import randint

class SunFlower(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('demo/SunFlower_0.png', PLANT_SIZE), 50)
        self.health = 40
        self.__last_produced = controller.level_ticks
        self.__cooldown_ticks = 15 * 60 # 15 seconds

    def update(self):
        now = controller.level_ticks
        if self.__last_produced + self.__cooldown_ticks <= now:
            self.__last_produced = now
            tile_rect = self.tile.rect
            sun = Sun()
            x_offset = int(tile_rect.width * 0.5)
            sun.rect.center = (randint(tile_rect.left + x_offset, tile_rect.right - x_offset), tile_rect.top + int(tile_rect.height * 0.2))
            sun.move_limit = tile_rect.height * 0.5
            self.scene.add_element(sun)

from components import controller