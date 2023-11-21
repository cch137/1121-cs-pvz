from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter, BulletTemplate
from components.media import media

class PeaShooter(Shooter):
    def __init__(self):
        Shooter.__init__(self, media.load_image(""))
        self.health = 100

pea1 = PeaShooter()
