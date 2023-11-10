from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability

class Plant: pass

all_plants: Set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Character):
    def __init__(self, image: pygame.Surface, abilities: Set[Ability] | None = None):
        Character.__init__(self, image, all_plants, all_zombies, abilities)

class BulletGenerator():
    def __init__(
            self,
            image: pygame.Surface,
            position: tuple[float, float] = (0.5, 0.5),
            velocity_x: int = 10,
            collision_damage: int = 0,
            collision_targets: Iterable[type[Entity] | Entity] = None,
            collision_effects: Iterable[Effect] = None,
            fire_sound: pygame.mixer.Sound = None,
            hit_sound: pygame.mixer.Sound = None,
            ):
        self.template = image
        self.position = position
        self.velocity_x = velocity_x
        self.collision_damage = collision_damage
        self.collision_targets = set(collision_targets or tuple())
        self.collision_effects = set(collision_effects or tuple())
        self.fire_sound = fire_sound
        self.hit_sound = hit_sound
        pygame.Surface((50, 50))
    
    def create(self, plant: Plant):
        bullet = Entity(self.template.copy(), self.collision_effects)
        bullet.allow_flyout = False
        bullet.velocity_x = self.velocity_x
        bullet.collision_damage = self.collision_damage
        for target in self.collision_targets:
            bullet.collision_targets.add(target)
        for effect in self.collision_effects:
            bullet.add_effect(effect)
        if self.fire_sound:
            self.fire_sound.play()
        bullet.z_index = 99
        bullet.rect.center = (
            plant.rect.x + plant.rect.width * self.position[0],
            plant.rect.y + plant.rect.height * self.position[1]
            )
        plant.scene.add_element(bullet)
        return bullet

class Shooter(Plant):
    def __init__(self, image: pygame.Surface, abilities: Set[Ability] | None = None):
        Plant.__init__(self, image, abilities)

from components.entities.zombies import all_zombies
