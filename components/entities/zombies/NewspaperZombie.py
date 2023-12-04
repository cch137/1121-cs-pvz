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

    def update(self):
        if self.health >= 100:
            self.move1()
        else:
            self.move2()