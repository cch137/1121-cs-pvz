from typing import *
import pygame
import components.character as character

class Plant(character.Character):
    def __init__(self, image: pygame.Surface):
        character.Character.__init__(self, image)
