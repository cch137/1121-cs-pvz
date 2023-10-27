from typing import *
import pygame
import utils.process as process
import components.element as element

class Character: pass

class Ability():
    def __init__(
            self,
            character: Character,
            name: str = '_',
            attack: int = 0,
            colddown: int = 60,
        ):
        self.character = character
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

class Character(element.Element):
    health: int = 100
    defense: int = 0
    '''number between 0 and 100'''

    def __init__(self, image: pygame.Surface):
        element.Element.__init__(self, image)
        self.abilities: set[Ability] = set()
    
    def damage(self, value: int):
        self.health -= value * (100 - self.defense)
    
    def update(self, *args: Any, **kargs: Any):
        element.Element.update(self, *args, **kargs)
        for ability in self.abilities:
            ability.use()

import components.character.plants as plants
import components.character.zombies as zombies
