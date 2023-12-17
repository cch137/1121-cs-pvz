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
        Zombie.__init__(
            self,
            media.load_image('zombies/newspaper_zombie.png', ZOMBIE_SIZE),
            media.load_image('zombies/newspaper_zombie_attack.png', ZOMBIE_SIZE),
            media.load_image('zombies/newspaper_zombie_speedup.png', ZOMBIE_SIZE),
        )
        self.health = 500
        self.move = zombie_mover(self)
        self.__last_attack = 0
        self.__cooldown_ticks = 60
    
    @property
    def is_angry(self):
        return self.health <= 200

    def update(self):
        now = controller.level_ticks
        if self.is_angry:
            match self.image_state:
                case 0: self.image = self.attack2_image
                case 1: self.image = self.attack1_image
                case 2: self.image = self.ori_image
        else:
            match self.image_state:
                case 0: self.image = self.ori_image
                case 1: self.image = self.attack1_image
                case 2: self.image = self.ori_image
        if self.image_state == 1 and self.__last_attack + 20 <= now:
            self.image_state = 2
        if self.image_state == 2 and self.__last_attack + 40 <= now:
            self.image_state = 0
        if self.has_seen_enemy(True, False):
            self.velocity_x = 0
            if self.__last_attack + self.__cooldown_ticks <= now:
                self.__last_attack = now
                self.image_state = 1
                self.closest_enemy.damage(25)
            return
        if self.image_state == 0:
            if self.is_angry:
                self.__cooldown_ticks = 40
                self.velocity_x = -2
            else:
                self.move()

from components import controller