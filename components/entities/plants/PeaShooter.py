from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie

class PeaShooter(Shooter):
    def __init__(self):
        Shooter.__init__(self, media.load_image(""), BulletTemplate(
            media.load_image("") , 
            (0.5, 0.5),
            (WINDOW_WIDTH/6),
            None,
            10,
            [Zombie]
        ))
        self.health = 40  

