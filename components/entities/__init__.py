from typing import *
import pygame
import utils.process as process
import components.element as element

class Entity: pass

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
        '''unit: second'''
        self.last_used_at: float = 0.0

    @property
    def is_cooling_down(self):
        return self.last_used_at + self.colddown > process.timestamp
    
    def use(self):
        if self.is_cooling_down: # 技能正在冷卻中，無法使用
            return
        if self.effect():
            self.last_used_at = process.timestamp

    def effect(self) -> bool:
        '''重寫此函式以賦予 Ability 效果。
        注意：此函式須返回一個布林值！布林值表示為此能力是否使用成功。'''
        return True

class Entity(element.Element):
    health: int = 100
    defense: int = 0
    '''number between 0 and 100'''
    vision_range: int = 3
    '''視野。單位：格(地圖 tile)'''

    def __init__(self, image: pygame.Surface):
        element.Element.__init__(self, image)
        self.abilities: set[Ability] = set()
    
    def damage(self, value: int):
        self.health -= value * (100 - self.defense)
    
    def update(self, *args: Any, **kargs: Any):
        element.Element.update(self, *args, **kargs)
        for ability in self.abilities:
            ability.use()

import components.entities.plants as plants
import components.entities.zombies as zombies
