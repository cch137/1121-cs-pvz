from typing import *
import pygame
from components.entities import Entity

class Zombie: pass

all_zombies: set[Zombie] = set()

import components.entities.plants as plants

class Zombie(Entity):
    def __init__(self, image: pygame.Surface):
        Entity.__init__(self, image)
        all_zombies.add(self)
    
    @property
    def closest_plant(self) -> plants.Plant:
        return

    @property
    def has_seen_zombies(self) -> bool:
        return

    def kill(self, *args: Any, **kargs):
        Entity.kill(self, *args, **kargs)
        all_zombies.remove(self)

from components.entities.plants import all_plants
