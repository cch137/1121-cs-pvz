from typing import Set, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect, Ability
import components.events as events

class Plant: pass

all_plants: Set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Character):
    def __init__(self, image: pygame.Surface):
        Character.__init__(self, image, all_plants, all_zombies)

class BulletTemplate():
    def __init__(
            self,
            image: pygame.Surface,
            position: tuple[float, float] = (0.5, 0.5),
            velocity_x: int = 10,
            background_color: ColorValue | None = None,
            collision_damage: int = 0,
            collision_targets: Iterable[type[Entity] | Entity] = None,
            collision_effects: Iterable[Effect] = None,
            fire_sound: pygame.mixer.Sound = None,
            hit_sound: pygame.mixer.Sound = None,
            ):
        self.template = image
        self.position = position
        self.velocity_x = velocity_x
        self.background_color = background_color
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
        bullet.background_color = self.background_color
        bullet.collision_damage = self.collision_damage
        for target in self.collision_targets:
            bullet.collision_targets.add(target)
        for effect in self.collision_effects:
            bullet.add_effect(effect)
        bullet.z_index = 99
        bullet.rect.center = (
            plant.rect.x + plant.rect.width * self.position[0],
            plant.rect.y + plant.rect.height * self.position[1]
            )
        plant.scene.add_element(bullet)
        if self.fire_sound:
            self.fire_sound.play()
        bullet.add_event_listener(events.KILL, lambda: self.hit_sound.play() if self.hit_sound else None)
        return bullet

class Shooter(Plant):
    def __init__(self, image: pygame.Surface, bullet_template: BulletTemplate):
        Plant.__init__(self, image)
        self.bullet_generator = bullet_template
    
    def shoot(self):
        self.bullet_generator.create(self)

from components.entities.zombies import all_zombies
