from typing import *
import pygame
import components.character as character

class Plant: pass

import components.character.zombies as zombies

class Plant(character.Character):
    def __init__(self, image: pygame.Surface):
        character.Character.__init__(self, image)
    
    @property
    def closest_zombie(self) -> zombies.Zombie:
        return

    @property
    def has_seen_plants(self) -> bool:
        return
