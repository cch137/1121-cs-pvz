from typing import Set
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events

class Zombie: pass

all_zombies: Set[Zombie] = set()

import components.entities.plants as plants

class Zombie(Character):
    def __init__(self, image: pygame.Surface):
        Character.__init__(self, image, all_zombies, all_plants)

from components.entities.plants import all_plants
