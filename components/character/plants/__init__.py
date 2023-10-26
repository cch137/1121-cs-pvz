from typing import *
import pygame
import components.character

class Plant(components.character.Character):
    def __init__(self, image: pygame.Surface):
        components.character.Character.__init__(self, image)
