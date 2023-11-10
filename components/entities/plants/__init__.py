from typing import Set
from utils.constants import *
import pygame
from components.entities import Character, Effect, Ability

class Plant: pass

all_plants: Set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Character):
    def __init__(self, image: pygame.Surface, abilities: Set[Ability] | None = None):
        Character.__init__(self, image, all_plants, all_zombies, abilities)

from components.entities.zombies import all_zombies
