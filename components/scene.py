from constants import *
from components.screen import screen
import pygame

class Scene(): pass

from components.element import Element

class Scene():
    def __init__(self, screen: pygame.Surface = screen):
        self.screen = screen

    background_color = BACKGROUND_COLOR

    __elements: set[Element] = set()

    @property
    def elements(self):
        return self.__elements

    layers: list[pygame.sprite.Group] = []

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
        '''注：你不需要手動調用此函數'''
        element_z_index = element.z_index
        while len(self.layers) <= element_z_index:
            self.layers.append(pygame.sprite.Group())
        self.layers[element_z_index].add(element)

    def _disconnect_element(self, element: Element):
        '''注：你不需要手動調用此函數'''
        self.layers[element.z_index].remove(element)
    
    def update(self):
        for layer in self.layers:
            layer.update()
    
    def compose(self):
        for layer in self.layers:
            for element in layer:
                element.compose()
    
    def draw(self):
        if self.background_color != None:
            # 設定視窗背景顏色
            self.screen.fill(self.background_color)
        for layer in self.layers:
            for element in layer:
                if element.background_color != None:
                    element.image.fill(element.background_color)
            layer.draw(screen)