from constants import *
import pygame

class Scene(): pass

from components.element import Element

class Scene():
    __elements: set[Element]
    layers: list[pygame.sprite.Group]

    def __init__(self, screen: pygame.Surface = None):
        self.screen = screen or controller.screen
        self.__elements = set()
        self.layers = list()

    def init(self):
        '''請覆蓋此方法。此方法將在第一次進入場景時建立調用以建立場景。'''
        pass

    background_color = BACKGROUND_COLOR

    @property
    def elements(self):
        return tuple(self.__elements)

    @property
    def is_playing(self):
        return controller.current_scene == self

    def get_element_by_id(self, id: str):
        for element in self.__elements:
            if element.id == id:
                return element
    
    def add_element(self, *elements: Element):
        for element in list(elements):
            self.__elements.add(element)
            element.connect_scene(self)
    
    def remove_element(self, *elements: Element):
        for element in list(elements):
            self.__elements.remove(element)
            self.disconnect_element(element)

    def connect_element(self, element: Element):
        '''注：此方法僅在 Element 內調用'''
        element_z_index = element.z_index
        while len(self.layers) <= element_z_index + 1:
            self.layers.append(pygame.sprite.Group())
        self.layers[element_z_index].add(element)

    def disconnect_element(self, element: Element):
        '''注：此方法僅在 Element 內調用'''
        self.layers[element.z_index].remove(element)
    
    def update(self):
        for layer in self.layers:
            layer.update()
    
    def compose(self):
        for element in self.elements:
            element.compose()
    
    def draw(self):
        if self.background_color != None:
            # 設定視窗背景顏色
            self.screen.fill(self.background_color)
        for layer in self.layers:
            for element in layer:
                if element.background_color != None:
                    element.image.fill(element.background_color)
            layer.draw(self.screen)

    def play(self):
        self.update()
        self.compose()
        self.draw()

from components.controller import controller
from components.scenes.main_menu import main_menu
from components.scenes.pause_menu import pause_menu
from components.scenes.main_game import main_game
from components.scenes.the_end import the_end
from components.scenes.testing1 import testing1
from components.scenes.testing2 import testing2
