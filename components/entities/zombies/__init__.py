from typing import *
import pygame
from components.entities import Entity

class Zombie: pass

import components.entities.plants as plants

class Zombie(Entity):
    def __init__(self, image: pygame.Surface):
        Entity.__init__(self, image)
    
    @property
    def closest_plant(self) -> plants.Plant:
        return

    @property
    def has_seen_zombies(self) -> bool:
        return
