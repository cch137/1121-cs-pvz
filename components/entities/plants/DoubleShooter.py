from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter, BulletTemplate, Shooter2
from components.media import media
from components.entities.zombies import Zombie

class DoubleShooter(Shooter,Shooter2):
    def __init__(self):
        Shooter.__init__(self, media.load_image(""), BulletTemplate(
            media.load_image("") 
            (0.5, 0.5),
            (WINDOW_WIDTH/5),
            (0,30,30),
            10,
            [Zombie]
            [None]
        ))

        Shooter2.__init__(self, media.load_image(""), BulletTemplate(
            media.load_image("")
            (0, 0.5),
            (WINDOW_WIDTH/5),
            (0,30,30),
            10,
            [Zombie]
            [None]
        ))

        self.health = 30
