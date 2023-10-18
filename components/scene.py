import pygame

class Scene(): pass

from components.element import *

class Scene():
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    __elements: set[Element] = set()

    def get_element_by_id(self, id: str):
        for element in self.__elements:
            if element.id == id:
                return element
    
    def add_element(self, element: Element):
        self.__elements.add(element)
    
    def remove_element(self, element: Element):
        self.__elements.remove(element)