from typing import *
from constants import *
import pygame
from components.entities import Character

class Plant: pass

all_plants: set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Character):
    def __init__(self, image: pygame.Surface):
        Character.__init__(self, image, all_plants, all_zombies)

from components.entities.zombies import all_zombies
