from utils.constants import *
from components.entities.plants import Plant 
from components.media import media
from components.entities.sun import Sun
import utils.process as process

class SunFlower(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('#原圖', (50, 50)), 50)
        self.health = 40
        self.__last_produced = process.ticks
        self.__cooldown_ticks = 15 * 60 # 15 seconds

    def update(self):
        now = process.ticks
        if now - self.__last_produced >= self.__cooldown_ticks:
            self.__last_produced = now
            centerx, centery = self.rect.center
            self.scene.add_element(Sun((centerx, centerx), (centery, centery)))
