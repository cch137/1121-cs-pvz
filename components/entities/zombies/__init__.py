from typing import *
import pygame
import components.entities as entities

class Zombie: pass

import components.entities.plants as plants

class Zombie(entities.Entity):
    def __init__(self, image: pygame.Surface):
        entities.Entity.__init__(self, image)
    
    @property
    def closest_plant(self) -> plants.Plant:
        return

    @property
    def has_seen_zombies(self) -> bool:
        return
