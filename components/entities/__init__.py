from typing import *
import pygame
import time
import math
import utils.process as process
from utils.timeout import set_timeout
from components import Element

class Effect: pass

class Entity: pass

class Effect():
    def __init__(self, name: str, durationTicks: int):
        '''name 屬性相同的 Effect 可以進行合併。\\
        即當一個實體被連續施加同一效果時，\\
        效果不會加重，但是持續時間會延長 (以最長的 durationSecs 為值)'''
        self.name = name
        self.durationTicks = durationTicks
        self.expired_at_tick = process.ticks + durationTicks

    def is_mergeable(self, other: Effect):
        return self.name == other.name

    def merge(self, other: Effect):
        self.durationTicks = max(self.durationTicks, other.durationSecs)
    
    def duplicate(self):
        return Effect(self.name, self.durationTicks)

    def apply(self, entity: Entity):
        entity.add_effect(self.duplicate())
    
    @property
    def is_expired(self):
        return self.durationTicks >= process.ticks

class SlowDownEffect(Effect):
    def __init__(self, name: str, durationTicks: int, rate: float):
        '''durationSecs 是效果持續的秒數。\\
        rate 是介於 0 到 1 之間的值。可以對目標的速度減緩。\\
        例如：目標原本速度為 `10`，rate 設為 `0.2`，目標修正後速度為 `8`'''
        Effect.__init__(self, name, durationTicks)
        self.rate = rate
    
    def duplicate(self):
        return SlowDownEffect(self.name, self.durationTicks, self.rate)

class PoisonEffect(Effect):
    def __init__(self, name: str, durationTicks: int, attack_power: int):
        '''durationSecs 是效果持續的秒數。\\
        attack_power 是每一幀對目標造成的傷害值。'''
        Effect.__init__(self, name, durationTicks)
        self.attack_power = attack_power
    
    def duplicate(self):
        return PoisonEffect(self.name, self.durationTicks, self.attack_power)

class Ability():
    def __init__(
            self,
            entities: Entity,
            name: str = '_',
            attack: int = 0,
            colddown: int = 60,
        ):
        self.entities = entities
        self.name = name
        self.attack = attack
        self.colddown = colddown
        '''unit: tick'''
        self.last_used_at: int = 0
        '''unit: tick'''

    @property
    def is_cooling_down(self):
        return self.last_used_at + self.colddown > process.ticks
    
    def use(self):
        if self.is_cooling_down: # 技能正在冷卻中，無法使用
            return
        if self.effect():
            self.last_used_at = process.ticks

    def effect(self) -> bool:
        '''重寫此函式以賦予 Ability 效果。
        注意：此函式須返回一個布林值！布林值表示為此能力是否使用成功。'''
        return True

class Entity(Element):
    health: int = 100
    '''本實體的生命值。注意：若要對本實體造成傷害，請使用 .damage()，不要直接更動此值。'''
    defense: int = 0
    '''number between 0 and 100'''
    vision_range: int = 3
    '''視野。單位：格(地圖 tile)'''
    velocity_x: int = 0
    velocity_y: int = 0
    acceleration_x: int = 0
    acceleration_y: int = 0
    move_limit: int | None = None
    '''實體的自動移動距離限制'''

    collision_target_types: set[type[[Entity]]]
    collision_damage: int | None = None
    '''與其他實體碰撞時，對該實體產生的傷害。若為 None 則不會與任何其他實體碰撞。'''

    def __init__(self, image: pygame.Surface):
        Element.__init__(self, image)
        self.abilities: set[Ability] = set()
        all_entities.add(self)
        self.collision_target_types = set()
        self.__self_effects: set[Effect] = set()
        '''此屬性是此實體身上目前所擁有的 Effect'''
        self.__damage_effects: set[Effect] = set()
        '''此屬性的 Effect 將在此實體對其他實體造成攻擊時，對其他實體所施加的效果。\\
        注意：如果要使用“子彈”對其他實體造成攻擊，你應該設置“子彈”的 Effect 而不是設置發出子彈的實體。'''
    
    def damage(self, value: int, *effects: Effect):
        '''對本實體造成傷害和效果。'''
        for effect in effects:
            self.add_effect(effect)
        self.health -= value * (1 - self.defense / 100)
        if self.dead:
            self.kill()
    
    @property
    def dead(self):
        return self.health <= 0
    
    def add_effect(self, effect: Effect):
        self.__self_effects.add(effect)
    
    def remove_effect(self, effect: Effect):
        self.__self_effects.remove(effect)
    
    def auto_update(self):
        # 處理效果
        slow_down_rate = 0
        for effect in tuple(self.__self_effects):
            if effect.is_expired:
                self.remove_effect(effect)
                continue
            if isinstance(effect, PoisonEffect):
                self.damage(effect.attack_power)
            elif isinstance(effect, SlowDownEffect):
                if effect.rate > slow_down_rate:
                    slow_down_rate = effect.rate
            effect.update()
        
        # 使用技能
        for ability in self.abilities:
            ability.use()

        if self.dead:
            return
        # 處理位移
        if self.move_limit is None or self.move_limit > 0:
            self.velocity_x += self.acceleration_x
            self.velocity_y += self.acceleration_y
            x1, y1 = self.x, self.y
            real_velocity_x = self.velocity_x * max(0, 1 - slow_down_rate)
            real_velocity_y = self.velocity_y * max(0, 1 - slow_down_rate)
            self.x += real_velocity_x
            self.y += real_velocity_y
            if self.move_limit is not None:
                self.move_limit -= math.sqrt(pow(self.x - x1, 2) + pow(self.y - y1, 2))
        
        # 判斷碰撞傷害
        if self.collision_damage is None or len(self.collision_target_types) == 0:
            return
        for entity in tuple(all_entities):
            if entity == self: continue
            for target_type in self.collision_target_types:
                if type(entity) is target_type and pygame.sprite.collide_circle(self, entity):
                    entity.damage(self.collision_damage, *[effect.duplicate() for effect in self.__damage_effects])
                    return self.kill()

    def kill(self, *args: Any, **kargs):
        Element.kill(self, *args, **kargs)
        all_entities.remove(self)

all_entities: set[Entity] = set()

import components.entities.plants as plants
import components.entities.zombies as zombies
