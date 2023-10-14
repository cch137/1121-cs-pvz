from typing import *
import pygame
from components.events import *

ROW = 'row'
COLUMN = 'column'
CELL = 'column'

class Element(): pass

class Element(pygame.sprite.Sprite):
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
        event_manager.addElement(self, eventName)

    def removeEventListener(self, eventName: str, listener: Callable):
        if eventName not in self.__listeners: return
        if listener not in self.__listeners[eventName]: return
        self.__listeners[eventName].remove(listener)
        if self.__listeners[eventName].__len__() == 0:
            event_manager.removeElement(self, eventName)

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

    __children = []
    __display = CELL

    '''Space between child elements.'''
    spacing: int = 0

    padding_top: int = 0
    padding_bottom: int = 0
    padding_left: int = 0
    padding_right: int = 0

    '''Padding between self and child elements.'''
    @property
    def padding(self):
        return (self.padding_left + self.padding_right + self.padding_top + self.padding_bottom) / 4

    @padding.setter
    def padding(self, value: int):
        self.padding_x = value
        self.padding_y = value
    
    @property
    def padding_x(self):
        return (self.padding_left + self.padding_right) / 2
    
    @padding_x.setter
    def padding_x(self, value: int):
        self.padding_left = value
        self.padding_right = value

    @property
    def padding_y(self):
        return (self.padding_top + self.padding_bottom) / 2

    @padding_y.setter
    def padding_y(self, value: int):
        self.padding_top = value
        self.padding_bottom = value

    @property
    def display(self):
        return self.__display

    @display.setter
    def display(self, value: str):
        if value not in (ROW, COLUMN):
            raise 'Invalid Element mode'
        self.__display = value

    @display.deleter
    def display(self):
        raise 'Element.mode cannot be deleted'
    
    def appendChild(self, *children: Element):
        for child in children:
            if child in self.__children:
                self.removeChild(child)
            self.__children.append(child)

    def removeChild(self, *children: Element):
        for child in children:
            if child in self.__children:
                self.__children.remove(child)
    
    def insertChild(self, index: int, *children: Element):
        children = tuple(reversed(children))
        for child in children:
            if child in self.__children:
                self.removeChild(child)
            self.__children.insert(index, child)
    
    def insertBefore(self, node: Element, *children: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node)
        children = tuple(reversed(children))
        for child in children:
            self.insertChild(index, child)
    
    def insertAfter(self, node: Element, child: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node) + 1
        children = tuple(reversed(children))
        for child in children:
            self.insertChild(index, child)        

class Character(Element):
    def __init__(self, image: pygame.Surface | tuple[int, int]):
        Element.__init__(image)

from components.event_manager import event_manager
