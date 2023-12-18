from utils.constants import *
from components.entities import Effect
from components.entities.plants import Plant, Planter
from components.media import media

health = 1000
price = 50
plant_cooldown_ticks = 10 * FPS

class WallNut(Plant):
    def __init__(self):
        rest_image = media.load_image('plants/wallnut.png', PLANT_SIZE)
        Plant.__init__(self, rest_image, price)
        self.rest_image = rest_image
        self.active_image = media.load_image('plants/wallnut_crying.png', PLANT_SIZE)
        self.health = health
    
    __is_crying: bool = False
    __cry_stop_tick: int = 0

    def damage(self, value: int, *effects: Effect):
        self.__is_crying = True
        self.__cry_stop_tick = controller.level_ticks + 120
        self.image = self.active_image
        return super().damage(value, *effects)

    def update(self):
        if self.__is_crying and self.__cry_stop_tick <= controller.level_ticks:
            self.image = self.rest_image
            self.__is_crying = False

planter = Planter(WallNut, price, plant_cooldown_ticks)

from components import controller