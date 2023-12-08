from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Plant
from components.media import media
from components.entities.zombies import Zombie, zombie_mover
import utils.process as process

class NewspaperZombie(Zombie):
    def __init__(self):
        Zombie.__init__(self, media.load_image('demo/NewspaperZombie_0.png', ZOMBIE_SIZE))
        self.health = 150
        self.move1 = zombie_mover(self)
        self.move2 = zombie_mover(self, -2)
        self.__last_attack = 0
        self.__cooldown_ticks = 60

    def update(self):
        now = controller.level_ticks
        if self.has_seen_enemy(True, False):
            self.velocity_x = 0
            if self.__last_attack + self.__cooldown_ticks <= now:
                self.__last_attack = now
                self.closest_enemy.damage(25)
            return
        if self.health >= 100:
            self.move1()
        else:
            self.move2()

from components import controller