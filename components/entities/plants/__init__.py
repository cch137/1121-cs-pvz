from typing import Set, Tuple, Iterable
from utils.constants import *
import pygame
from components.entities import Entity, Character, Effect
import components.events as events
import utils.process as process

class Plant: pass

all_plants: Set[Plant] = set()

import components.entities.zombies as zombies

class Plant(Character):
    def __init__(self, image: pygame.Surface, price: int):
        Character.__init__(self, image, all_plants, all_zombies)
        self.price = price

    @property
    def tile(self):
        return self.parent

class Shooter(Plant):
    shoot_position: Tuple[float, float]

class BulletTemplate():
    def __init__(
            self,
            image: pygame.Surface,
            velocity_x: int = 10,
            background_color: ColorValue | None = None,
            collision_damage: int = 0,
            collision_targets: Iterable[type[Entity] | Entity] = None,
            collision_effects: Iterable[Effect] = None,
            fire_sound: pygame.mixer.Sound = None,
            hit_sound: pygame.mixer.Sound = None,
            ):
        self.template = image
        self.velocity_x = velocity_x
        self.background_color = background_color
        self.collision_damage = collision_damage
        self.collision_targets = set(collision_targets or tuple())
        self.collision_effects = set(collision_effects or tuple())
        self.fire_sound = fire_sound
        self.hit_sound = hit_sound
    
    def create(self, plant: Shooter):
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
            plant.rect.x + plant.rect.width * plant.shoot_position[0],
            plant.rect.y + plant.rect.height * plant.shoot_position[1]
            )
        plant.scene.add_element(bullet)
        if self.fire_sound:
            self.fire_sound.play()
        bullet.add_event_listener(events.KILL, lambda: self.hit_sound.play() if self.hit_sound else None)
        return bullet

class Shooter(Plant):
    def __init__(
        self,
        image: pygame.Surface,
        price: int,
        shoot_position: Tuple[float, float],
        bullet_template: BulletTemplate,
        attack_frequency_ticks: int = 60
    ):
        Plant.__init__(self, image, price)
        self.__last_shoot_tick = process.ticks
        self.shoot_position = shoot_position
        '''從左上角到右下角的比例，子彈以該點作為中心發射。'''
        self.bullet_generator = bullet_template
        self.attack_frequency_ticks = attack_frequency_ticks

    def shoot(self):
        self.bullet_generator.create(self, self.shoot_position)

    def update(self):
        if not self.has_seen_enemy(False, True):
            return
        now = process.ticks
        if self.__last_shoot_tick + self.attack_frequency_ticks <= now:
            self.__last_shoot_tick = now
            self.shoot()

from components.entities.zombies import all_zombies
