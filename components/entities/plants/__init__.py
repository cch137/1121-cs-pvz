from typing import *
import pygame
from components.entities import Entity

class Plant: pass

all_plants: set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Entity):
    def __init__(self, image: pygame.Surface):
        Entity.__init__(self, image)
        all_plants.add(self)
    
    @property
    def closest_zombie(self) -> zombies.Zombie:
        return

    @property
    def has_seen_plants(self) -> bool:
        return

    def kill(self, *args: Any, **kargs):
        Entity.kill(self, *args, **kargs)
        all_plants.remove(self)

from components.entities.zombies import all_zombies
