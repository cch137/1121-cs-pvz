from typing import *
import pygame
from components.entities import Entity

class Plant: pass

import components.entities.zombies as zombies

class Plant(Entity):
    def __init__(self, image: pygame.Surface):
        Entity.__init__(self, image)
    
    @property
    def closest_zombie(self) -> zombies.Zombie:
        return

    @property
    def has_seen_plants(self) -> bool:
        return
