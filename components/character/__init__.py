from typing import *
import pygame
import components.element

class Character(components.element.Element):
    def __init__(self, image: pygame.Surface):
        components.element.Element.__init__(self, image)
