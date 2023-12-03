from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie
import utils.asynclib as asynclib

class DoubleShooter(Shooter):
    def __init__(self):
        Shooter.__init__(self, media.load_image(""), BulletTemplate(
            media.load_image("") 
            (0.5, 0.5),
            (WINDOW_WIDTH/5),
            None,
            10,
            [Zombie]
        ))
        self.health = 30
    
    def shoot(self):
        Shooter.shoot(self)
        asynclib.set_timeout(lambda: Shooter.shoot(self), 200)
