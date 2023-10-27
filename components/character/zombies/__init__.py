from typing import *
import pygame
import components.character as character

class Zombie: pass

import components.character.plants as plants

class Zombie(character.Character):
    def __init__(self, image: pygame.Surface):
        character.Character.__init__(self, image)
    
    @property
    def closest_plant(self) -> plants.Plant:
        return

    @property
    def has_seen_zombies(self) -> bool:
        return
