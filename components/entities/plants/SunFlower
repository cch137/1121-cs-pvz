from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter 
from components.media import media
from components.entities.zombies import Zombie
from components.entities.sun import Sun

class SunFlower(Shooter):
    def __init__(self):
        self.health = 40 
        self = pygame.load.image(os.path.join("asserts","plants","")).convert()
        self.set_time = 0

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.set_time >= 6000 :
            self.set_time = now
            DropSun =  Sun(SunFlower.rect.center)
