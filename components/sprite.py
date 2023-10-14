from typing import *
import pygame
from components.events import *

class Sprite(pygame.sprite.Sprite):
    __attributes = {}
    __listeners: dict[str, set[Callable]] = {}
    
    bg_color: str = None

    def __init__(self, image: pygame.Surface | tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        if type(image) == pygame.Surface:
            self.image = image
        elif type(image) == tuple:
            if type(image[0]) == int and type(image[1]) == int:
                self.image = pygame.Surface((image[0], image[1]))
        else:
            raise 'Invalid image'
        self.rect = self.image.get_rect()

    def addEventListener(self, eventName: str, listener: Callable):
        if eventName not in self.__listeners:
            self.__listeners[eventName] = set()
        self.__listeners[eventName].add(listener)
        event_manager.addSprite(self, eventName)

    def removeEventListener(self, eventName: str, listener: Callable):
        if eventName not in self.__listeners: return
        if listener not in self.__listeners[eventName]: return
        self.__listeners[eventName].remove(listener)
        if self.__listeners[eventName].__len__() == 0:
            event_manager.removeSprite(self, eventName)

    def dispatchEvent(self, event: UserEvent):
        if event.name in self.__listeners:
            for listener in self.__listeners[event.name]:
                try:
                    if listener.__code__.co_argcount > 0: listener(event)
                    else: listener()
                except Exception as err:
                    print(err)

    def getAttribute(self, name: str):
        return self.__attributes.get(name)

    def setAttribute(self, name: str, value):
        self.__attributes[name] = value
    
    def removeAttribute(self, name: str):
        del self.__attributes[name]
    
    def hasAttribute(self, name: str):
        return name in self.__attributes

class Grid(Sprite):
    def __init__(self, image: pygame.Surface | tuple[int, int]):
        Sprite.__init__(image)
    pass

class Character(Sprite):
    def __init__(self, image: pygame.Surface | tuple[int, int]):
        Sprite.__init__(image)
    pass

from components.event_manager import event_manager
