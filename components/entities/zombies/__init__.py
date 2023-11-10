from typing import *
from utils.constants import *
import pygame
from components.entities import Character, Effect, Ability

class Zombie: pass

all_zombies: set[Zombie] = set()

import components.entities.plants as plants

class Zombie(Character):
    def __init__(self, image: pygame.Surface, abilities: set[Ability] | None = None):
        Character.__init__(self, image, all_zombies, all_plants, abilities)

from components.entities.plants import all_plants
