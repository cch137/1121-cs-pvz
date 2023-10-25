from constants import *
from components.screen import screen
import pygame

class Scene(): pass

from components.element import *

class Scene():
    def __init__(self, screen: pygame.Surface = screen):
        self.screen = screen

    background_color = BACKGROUND_COLOR

    __elements: set[Element] = set()

    layers: list[pygame.sprite.Group[Element]] = []

    def get_element_by_id(self, id: str):
        for element in self.__elements:
            if element.id == id:
                return element
    
    def add_element(self, element: Element):
        self.__elements.add(element)
        self._connect_element(element)
    
    def remove_element(self, element: Element):
        self.__elements.remove(element)
        self._disconnect_element(element)

    def _connect_element(self, element: Element):
        '''你不需要手動調用此函數， add_element 會自動 connect 該 element 和其 children'''
        element_layer = element.layer
        while len(self.layers) <= element_layer:
            self.layers.append(pygame.sprite.Group())
        self.layers[element_layer].add(element)

    def _disconnect_element(self, element: Element):
        '''你不需要手動調用此函數， remove_element 會自動 disconnect 該 element 和其 children'''
        self.layers[element.layer].remove(element)
    
    def update(self):
        for layer in self.layers:
            layer.update()
    
    def draw(self):
        if self.background_color != None:
            self.screen.fill(self.background_color)
        for layer in self.layers:
            for element in layer:
                if element.background_color != None:
                    element.image.fill(element.background_color)
            layer.draw()