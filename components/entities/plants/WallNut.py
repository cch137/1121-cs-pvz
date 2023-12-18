from utils.constants import *
from components.entities import Effect
from components.entities.plants import Plant, Planter
from components.media import media

health = 1000
price = 50
plant_cooldown_ticks = 20 * FPS

class WallNut(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('plants/wallnut.png', PLANT_SIZE), price)
        self.crying_image = media.load_image('plants/wallnut_crying.png', PLANT_SIZE)
        self.health = health

    __is_crying: bool = False

    def damage(self, value: int, *effects: Effect):
        super().damage(value, *effects)
        if not self.__is_crying and self.health < 0.35 * health:
            self.image = self.crying_image
            self.__is_crying = True

planter = Planter(WallNut, price, plant_cooldown_ticks)

from components import controller