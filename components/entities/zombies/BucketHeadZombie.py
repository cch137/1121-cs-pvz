from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Plant
from components.media import media
from components.entities.zombies import Zombie, zombie_mover
import utils.process as process

class BucketHeadZombie(Zombie):
    def __init__(self):
        Zombie.__init__(
            self,
            media.load_image('zombies/buckethead_zombie.png', ZOMBIE_SIZE),
            media.load_image('zombies/buckethead_zombie_attack_1.png', ZOMBIE_SIZE),
            media.load_image('zombies/buckethead_zombie_attack_2.png', ZOMBIE_SIZE),
        )
        self.is_buckethead = True
        self.health = 800
        self.move = zombie_mover(self)
        self.__last_attack = 0
        self.__cooldown_ticks = 60

    def update(self):
        now = controller.level_ticks
        match self.image_state:
            case 0: self.image = self.ori_image
            case 1: self.image = self.attack1_image
            case 2: self.image = self.attack2_image
        if self.image_state == 1 and self.__last_attack + 20 <= now:
            self.image_state = 2
        if self.image_state == 2 and self.__last_attack + 40 <= now:
            self.image_state = 0
        if self.is_buckethead and self.health <= 300:
            self.ori_image = media.load_image('zombies/zombie.png', ZOMBIE_SIZE)
            self.attack1_image = media.load_image('zombies/zombie_attack_1.png', ZOMBIE_SIZE)
            self.attack2_image = media.load_image('zombies/zombie_attack_2.png', ZOMBIE_SIZE)
            self.is_buckethead = False
        if self.has_seen_enemy(True, False):
            self.velocity_x = 0
            if self.__last_attack + self.__cooldown_ticks <= now:
                self.__last_attack = now
                self.image_state = 1
                self.closest_enemy.damage(25)
            return
        if self.image_state == 0:
            self.move()

from components import controller