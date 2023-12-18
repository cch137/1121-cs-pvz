from utils.constants import *
from components.entities.plants import Plant, Planter
from components.media import media
from components.entities.Sun import Sun
from random import randint

health = 50
price = 50
plant_cooldown_ticks = 5 * FPS

class SunFlower(Plant):
    def __init__(self):
        rest_image = media.load_image('plants/sunflower.png', PLANT_SIZE)
        Plant.__init__(self, rest_image, price)
        self.rest_image = rest_image
        self.active_image = media.load_image('plants/sunflower_uuewk.png', PLANT_SIZE)
        self.__is_activated = False
        self.health = health
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
            self.image = self.active_image
            self.__is_activated = True
        if self.__is_activated and self.__last_produced + 60 <= now:
            self.image = self.rest_image
            self.__is_activated = False

planter = Planter(SunFlower, price, plant_cooldown_ticks)

from components import controller