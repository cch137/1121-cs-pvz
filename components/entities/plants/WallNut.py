from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Plant, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie
import utils.process as process

class WallNut(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('#原圖', (50, 50)))
        self.health = 100
    
    __is_crying: bool = False
    __cry_stop_tick: int = 0

    def damage(self, value: int, *effects: Effect):
        self.__is_crying = True
        self.__cry_stop_tick = process.ticks + 30
        # 設置哭泣的圖片
        self.image = media.load_image('#哭哭圖', ())
        return super().damage(value, *effects)

    def update(self):
        if self.__is_crying:
            if process.ticks < self.__cry_stop_tick:
                self.image = media.load_image('#原圖', ())
                self.__is_crying = False