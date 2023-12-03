from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Plant
from components.media import media
from components.entities.zombies import Zombie
import utils.process as process

class BucketHeadZombie(Zombie):
    def __init__(self):
        Zombie.__init__(self, media.load_image('#原圖', (50, 50)))
        self.health = 100

    def update(self):
        pass