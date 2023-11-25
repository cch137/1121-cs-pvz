from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie

class bomb(Shooter):
    def __init__(self):
        Shooter.__init__(0)
        #這邊我的想法是 不賦予子彈 然後bomb在有殭屍進入他九宮格範圍後會攻擊一次然後死掉 
        pygame.sprite.groupcollide(self,Zombie,True,False)
        self.health = 20