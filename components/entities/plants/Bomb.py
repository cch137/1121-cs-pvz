from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Plant, BulletTemplate, all_plants, all_zombies
from components.media import media
from components.entities.zombies import Zombie
import utils.asynclib as asynclib

class ReadyToExplosion(Character):
    def __init__(self):
        Character.__init__(self, media.load_image('#原圖', (50, 50)), all_plants, all_zombies)
        asynclib.set_timeout(lambda: self.bomb(), 2000)

    def bomb(self):
        for enemy in self.enemies_in_radius(TILE_WIDTH):
            enemy.kill()
        self.image = media.load_image('#爆炸', (50, 50))
        asynclib.set_timeout(lambda: self.kill(), 1000)

class Bomb(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('#原圖', (50, 50)))
        self.health = 1000
        self.fov = 0.25 * TILE_WIDTH

    def auto_update(self):
        if self.has_seen_enemy(True, True):
            self.kill()
            self.tile.append_child(ReadyToExplosion())
