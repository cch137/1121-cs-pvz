from utils.constants import *
from components.entities import Effect
from components.entities.plants import Plant
from components.media import media
import utils.process as process

class WallNut(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('demo/WallNut_0.png', PLANT_SIZE), 50)
        self.health = 500
    
    __is_crying: bool = False
    __cry_stop_tick: int = 0

    def damage(self, value: int, *effects: Effect):
        self.__is_crying = True
        self.__cry_stop_tick = process.ticks + 30
        # 設置哭泣的圖片
        self.image = media.load_image('demo/WallNut_0.png', PLANT_SIZE)
        return super().damage(value, *effects)

    def update(self):
        if self.__is_crying:
            if process.ticks < self.__cry_stop_tick:
                self.image = media.load_image('demo/WallNut_0.png', PLANT_SIZE)
                self.__is_crying = False