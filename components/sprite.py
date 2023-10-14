import pygame

class Sprite(pygame.sprite.Sprite):
    listeners: dict[str, set[function]] = {}
    bg_color: str = None

    def __init__(self, image: pygame.Surface | (int, int)):
        if type(image) == pygame.Surface:
            self.image = image
        elif type(image) == tuple:
            if type(image[0]) == int and type(image[1]) == int:
                self.image = pygame.Surface((image[0], image[1]))
        else:
            raise 'Invalid image'
        self.rect = self.image.get_rect()

    def addEventListener(self, event: str, listener: function):
        if event not in self.listeners:
            self.listeners[event] = set()
        self.listeners[event].add(listener)
        eventManager.addSprite(self, event)

    def removeEventListener(self, event: str, listener: function):
        if event not in self.listeners: return
        if listener not in self.listeners[event]: return
        self.listeners[event].remove(listener)
        if self.listeners[event].__len__() == 0:
            eventManager.removeSprite(self, event)

    def dispatchEvent(self, event: str):
        if event not in self.listeners: return
        for listener in self.listeners[event]:
            try: listener()
            except: pass

class Grid(Sprite):
    pass

class Character(Sprite):
    pass

from eventManager import eventManager