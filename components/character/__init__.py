from typing import *
import pygame
import components.element as element

class Character(element.Element):
    def __init__(self, image: pygame.Surface):
        element.Element.__init__(self, image)

import components.character.plants as plants
import components.character.zombies as zombies
