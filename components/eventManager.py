import pygame
from components import Sprite

class EventManager():
    listeners: dict[str, pygame.sprite.Group] = {}

    def addSprite(self, sprite: Sprite, event: str):
        if event not in self.listeners:
            self.listeners[event] = pygame.sprite.Group()
        self.listeners[event].add(sprite)

    def removeSprite(self, sprite: Sprite, event: str):
        if event in self.listeners:
            if self.listeners[event].has(sprite):
                self.listeners[event].remove(sprite)
    
    def run(self):
        pass

eventManager = EventManager()