from typing import *
import pygame
import components.entities as entities

class Plant: pass

import components.entities.zombies as zombies

class Plant(entities.Entity):
    def __init__(self, image: pygame.Surface):
        entities.Entity.__init__(self, image)
    
    @property
    def closest_zombie(self) -> zombies.Zombie:
        return

    @property
    def has_seen_plants(self) -> bool:
        return
