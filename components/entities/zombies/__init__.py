from typing import Set
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events

class Zombie: pass

all_zombies: Set[Zombie] = set()

import components.entities.plants as plants

class Zombie(Character):
    def __init__(self, ori_image: pygame.Surface, attack1_image: pygame.Surface, attack2_image: pygame.Surface):
        Character.__init__(self, ori_image, all_zombies, all_plants)
        all_zombies.add(self)
        self.z_index = 999999
        self.image_state: int = 0
        self.ori_image = ori_image
        self.attack1_image = attack1_image
        self.attack2_image = attack2_image
        self.radius_scale = 0.25
        self.fov = 30
    
    def auto_update(self):
        Character.auto_update(self)
        if self.rect.right < 0:
            controller.level.victory = False
            controller.goto_scene(controller.scenes.the_end)
            controller.unload_sceen(controller.scenes.main_game)

def zombie_mover(zombie: Zombie, rate: float = -0.75):
    zombie.velocity_x = 0
    sleeping = 0
    velocity_sign = 0
    if rate < 0: velocity_sign = 1
    forward = True
    a = 0.6 * rate
    b = -0.1 * rate
    def zombie_move():
        nonlocal sleeping
        nonlocal velocity_sign
        nonlocal forward
        if sleeping < 60:
            sleeping += 1
            return
        if rate >= 0:
            if velocity_sign == 0 and zombie.velocity_x < 0:
                velocity_sign = 1
            elif velocity_sign == 1 and zombie.velocity_x >= 0:
                velocity_sign = 0
                sleeping = 0
                zombie.velocity_x = 0
                return
        else:
            if velocity_sign == 0 and zombie.velocity_x <= 0:
                velocity_sign = 1
                sleeping = 0
                zombie.velocity_x = 0
                return
            elif velocity_sign == 1 and zombie.velocity_x > 0:
                velocity_sign = 0
        if forward:
            if (rate >= 0 and zombie.velocity_x < a) or (rate < 0 and zombie.velocity_x > a):
                zombie.velocity_x += 0.0125 * rate
            else:
                forward = False
        else:
            if (rate >= 0 and zombie.velocity_x > b) or (rate < 0 and zombie.velocity_x < b):
                zombie.velocity_x -= 0.0125 * rate
            else:
                forward = True
    return zombie_move

from components.entities.plants import all_plants

from components.entities.zombies.RegularZombie import RegularZombie
from components.entities.zombies.BucketHeadZombie import BucketHeadZombie
from components.entities.zombies.NewspaperZombie import NewspaperZombie

from components import controller
