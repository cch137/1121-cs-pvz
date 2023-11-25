from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie

class Nut(Shooter):
    def __init__(self):
        self.health = 100
        self = pygame.load.image(os.path.join("asserts","plants","")).convert()

         