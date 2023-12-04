from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Plant
from components.media import media
from components.entities.zombies import Zombie, zombie_mover

class RegularZombie(Zombie):
    def __init__(self):
        Zombie.__init__(self, media.load_image('demo/Zombie_0.png', ZOMBIE_SIZE))
        self.health = 100
        self.move = zombie_mover(self)

    def update(self):
        self.move()
        #還沒有攻擊