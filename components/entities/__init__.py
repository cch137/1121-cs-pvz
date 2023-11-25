import pygame
import math
import utils.process as process
from typing import Set, Any
from utils.constants import *
from components import Element
from pygame.transform import rotate

class Effect: pass

class Entity: pass

class Effect():
    def __init__(self, name: str, durationTicks: int):
        '''name 屬性相同的 Effect 可以進行合併。\\
        即當一個實體被連續施加同一效果時，\\
        效果不會加重，但是持續時間會延長 (以最長的 duration_ticks 為值)'''
        self.name = name
        self.duration_ticks = durationTicks
        self.expired_at_tick = process.ticks + durationTicks

    def is_mergeable(self, other: Effect):
        return self.name == other.name

    def merge(self, other: Effect):
        self.duration_ticks = max(self.duration_ticks, other.duration_ticks)

    def duplicate(self):
        return Effect(self.name, self.duration_ticks)

    def apply(self, entity: Entity):
        entity.add_effect(self.duplicate())

    @property
    def is_expired(self):
        return self.expired_at_tick <= process.ticks

class SlowDownEffect(Effect):
    def __init__(self, name: str, duration_ticks: int, rate: float):
        '''duration_ticks 是效果持續的幀數。\\
        rate 是介於 0 到 1 之間的值。可以對目標的速度減緩。\\
        例如：目標原本速度為 `10`，rate 設為 `0.2`，目標修正後速度為 `8`'''
        Effect.__init__(self, name, duration_ticks)
        self.rate = rate

    def duplicate(self):
        return SlowDownEffect(self.name, self.duration_ticks, self.rate)

class PoisonEffect(Effect):
    def __init__(self, name: str, duration_ticks: int, attack_power: int):
        '''duration_ticks 是效果持續的幀數。\\
        attack_power 是每一幀對目標造成的傷害值。'''
        Effect.__init__(self, name, duration_ticks)
        self.attack_power = attack_power

    def duplicate(self):
        return PoisonEffect(self.name, self.duration_ticks, self.attack_power)

class Ability():
    def __init__(self, colddown: int = 60):
        self.colddown = colddown
        '''unit: tick'''
        self.last_used_at: int = 0
        '''unit: tick'''

    @property
    def is_cooling_down(self):
        return self.last_used_at + self.colddown > process.ticks

    def use(self, entity: Entity):
        if self.is_cooling_down: # 技能正在冷卻中，無法使用
            return
        if self.effect.__code__.co_argcount > 0:
            if self.effect(entity):
                self.last_used_at = process.ticks
        elif self.effect():
            self.last_used_at = process.ticks

    def effect(self, entity: Entity) -> bool:
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
    velocity_a: int = 0
    acceleration_x: int = 0
    acceleration_y: int = 0
    acceleration_a: int = 0
    move_limit: int | None = None
    '''實體的自動移動距離限制'''

    collision_targets: Set[type[Entity]|Entity]
    '''collision_targets 中的項目可以是 class 或者指定的實體。\\
    若目標屬於 class ，當此實體和該 class 的實體碰撞時會對其造成傷害。\\
    若目標屬於指定實體，當此實體和該指定實體碰撞時會對其造成傷害。'''

    collision_damage: int | None = None
    '''與其他實體碰撞時，對該實體產生的傷害。若為 None 則不會與任何其他實體碰撞。'''

    def __init__(self, image: pygame.Surface,
        collision_effects: Set[Effect] | None = None, abilities: Set[Ability] | None = None):
        '''collision_effects 是當實體與其他實體碰撞後對該實體所產生的效果 (若實體為可碰撞的)\\
        abilities 是技能'''
        Element.__init__(self, image)

        self.abilities = abilities or set()
        all_entities.add(self)
        self.collision_targets = set()

        self.__self_effects: Set[Effect] = set()
        '''此屬性是此實體身上目前所擁有的 Effect'''

        self.__collision_effects = collision_effects or set()
        '''此屬性的 Effect 將在此實體對其他實體造成攻擊時，對其他實體所施加的效果。\\
        注意：如果要使用“子彈”對其他實體造成攻擊，你應該設置“子彈”的 Effect 而不是設置發出子彈的實體。'''

    image_0: pygame.Surface | None = None

    def clear_image_0(self):
        self.image_0 = None

    __rotation_angle: int = 0

    @property
    def rotation_angle(self):
        return self.__rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, angle: int):
        if self.image_0 is None:
            self.image_0 = self.image.copy()
        self.__rotation_angle = angle % 360
        center = self.rect.center
        self.image = rotate(self.image_0, self.__rotation_angle)
        self.rect.center = center

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
        velocity_rate = max(0, 1 - slow_down_rate)
        
        # 使用技能
        for ability in self.abilities:
            ability.use(self)

        if self.dead:
            return
        # 處理位移
        if self.move_limit is None or self.move_limit > 0:
            rect = self.rect
            x1, y1 = rect.x, rect.y
            real_velocity_x = self.velocity_x * velocity_rate
            real_velocity_y = self.velocity_y * velocity_rate
            rect.x += real_velocity_x
            rect.y += real_velocity_y
            if self.move_limit is not None:
                self.move_limit -= math.dist((rect.x, rect.y), (x1, y1))
            self.velocity_x += self.acceleration_x
            self.velocity_y += self.acceleration_y
        # 處理旋轉
        if self.velocity_a:
            self.rotation_angle += self.velocity_a * velocity_rate
            self.velocity_a += self.acceleration_a
        
        if isinstance(self, Character) and self.is_touch_with_enemy:
            return # 遊戲角色會被敵人阻擋，於是無法前進
        
        # 判斷碰撞傷害
        if self.collision_damage is None or len(self.collision_targets) == 0:
            return
        for entity in tuple(all_entities):
            if entity == self: continue
            for target in self.collision_targets:
                if (type(target) is type and type(entity) is target) or target is entity:
                    if pygame.sprite.collide_circle(self, entity):
                        entity.damage(self.collision_damage, *[effect.duplicate() for effect in self.__collision_effects])
                        return self.kill()
                elif entity == target:
                    entity.damage(self.collision_damage, *[effect.duplicate() for effect in self.__collision_effects])
                    return self.kill()

    def dist(self, target: Entity):
        return math.dist(self.rect.center, target.rect.center)

    def kill(self, *args: Any, **kargs):
        Element.kill(self, *args, **kargs)
        all_entities.remove(self)

all_entities: Set[Entity] = set()

class Character: pass

class Character(Entity):
    fov = TILE_WIDTH * 3
    '''視野範圍（單位：像素）'''

    def __init__(self, image: pygame.Surface, friends: Set[Character], enemies: Set[Character], abilities: Set[Ability] | None = None):
        '''角色'''
        Entity.__init__(self, image, None, abilities)
        friends.add(self)
        self.__friends = friends
        self.__enemies = enemies

    @property
    def friends(self):
        return set(f for f in self.__friends if f is not self)

    @property
    def enemies(self):
        return set(f for f in self.__enemies if f is not self)
    
    def __closest_from_set(self, character_set: Set[Character]):
        if len(character_set) == 0: return None
        try: return min(character_set, key=lambda x: self.dist(x))
        except: return None
    
    @property
    def closest_enemy(self):
        return self.__closest_from_set(self.enemies)
    
    @property
    def enemies_on_row(self):
        return tuple(i for i in self.enemies if self.is_on_same_horizontal(i))
    
    @property
    def closest_enemy_on_row(self):
        return self.__closest_from_set(set(self.enemies_on_row))
    
    def enemies_in_radius(self, radius: int):
        return tuple(i for i in self.enemies if self.dist(i) < radius)

    @property
    def is_touch_with_enemy(self):
        return pygame.sprite.collide_circle(self, self.closest_enemy_on_row) \
            or pygame.sprite.collide_circle(self, self.closest_enemy)
    
    def is_on_same_horizontal(self, other: Character):
        other_rect: pygame.Rect = other.rect.center
        self_rect = self.rect
        return (self_rect.top < other_rect.centery and self_rect.bottom > other_rect.centery) \
            or (other_rect.top < self_rect.centery and other_rect.bottom > self_rect.centery)
    
    def is_on_same_vertical(self, other: Character):
        other_rect: pygame.Rect = other.rect.center
        self_rect = self.rect
        return (self_rect.left < other_rect.centerx and self_rect.right > other_rect.centerx) \
            or (other_rect.left < self_rect.centerx and other_rect.right > self_rect.centerx)

    def in_fov(self, other: Character):
        '''判斷 other 是否位於視野範圍內。'''
        return self.dist(other) <= self.fov

    def has_seen_enemy(self, on_left: bool = False, on_right: bool = False):
        '''on_left 判斷是否左方有敵人，on_right 判斷是否右方有敵人。\\
        二者皆 True 則其中一方有敵人即返回 True。'''
        if not (on_left or on_right):
            return False
        for char in self.enemies:
            if char == self or not self.is_on_same_horizontal(char) or not self.in_fov(char):
                continue
            if on_left and self.rect.centerx > char.rect.centerx:
                return True
            if on_right and self.rect.centerx < char.rect.centerx:
                return True
        return False

    def kill(self, *args: Any, **kargs):
        Entity.kill(self, *args, **kargs)
        self.__friends.remove(self)

import components.entities.plants as plants
import components.entities.zombies as zombies
from components.entities.sun import Sun
