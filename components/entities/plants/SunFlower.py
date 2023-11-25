from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Plant 
from components.media import media
from components.entities.zombies import Zombie
from components.entities.sun import Sun
import utils.process as process

class SunFlower(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('#原圖', (50, 50)))
        self.health = 40
        self.__spawned_tick = process.ticks

    def auto_update(self):
        Entity.auto_update(self)
        now = process.ticks
        centerx, centery = self.rect.center
        if now - self.__spawned_tick >= 600:
            self.__spawned_tick = now
            self.scene.add_element(Sun((centerx, centerx), (centery, centery), 10))
