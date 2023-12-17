from typing import Set, Dict
from utils.constants import *
import pygame
import components.element as element

class Scene():
    __elements: Set[element.Element]
    layers: Dict[int, pygame.sprite.Group]

    def __init__(self, screen: pygame.Surface = None):
        self.screen = screen or controller.screen
        self.__elements = set()
        self.layers = dict()

    background_color = BACKGROUND_COLOR
    
    background_music: str | bool | None = None
    '''背景音樂的文件路徑，以根目錄為相對路徑。\\
    為 None 延續上一個背景音樂。\\
    為 True 終止背景音樂，該音樂在下次切入時在暫停點繼續。\\
    為 False 為無背景音樂，該音樂在下次切入時重播。
    '''

    background_music_volume: float = 1
    '''從 0 到 1 的音量比值。'''

    @property
    def all_elements(self):
        for _, layer in self.layers.items():
            for element in layer:
                yield element

    @property
    def is_playing(self):
        return controller.current_scene == self

    def init(self):
        '''請覆蓋此方法。此方法將在第一次進入場景時調用以建立場景。'''
        pass

    def get_element_by_id(self, id: str) -> element.Element | None:
        for el in self.all_elements:
            if el.id == id:
                return el

    def add_element(self, *elements: element.Element):
        El = element.Element
        for el in elements:
            if not isinstance(el, El):
                continue
            self.__elements.add(el)
            el.connect_scene(self)

    def remove_element(self, *elements: element.Element):
        for element in elements:
            self.__elements.remove(element)
            self.disconnect_element(element)

    def connect_element(self, element: element.Element):
        '''注：此方法僅在 Element 內調用'''
        self.layers.setdefault(element.z_index, pygame.sprite.Group()).add(element)

    def disconnect_element(self, element: element.Element):
        '''注：此方法僅在 Element 內調用'''
        if element in self.__elements:
            self.__elements.remove(element)
        z = element.z_index
        if z in self.layers:
            self.layers[z].remove(element)
            if len(self.layers[z]) == 0:
                del self.layers[z]

    def reconnect_element(self, element: element.Element):
        '''注：此方法僅在 Element 內調用'''
        self.disconnect_element(element)
        self.connect_element(element)

    def update(self):
        import components.entities as entities
        for layer in tuple(self.layers.values()):
            for el in layer:
                if isinstance(el, entities.Entity):
                    try: el.auto_update()
                    except Exception as e: print(el, 'auto update error:', e)
                    if not el.updateable:
                        el.updateable = True
                        continue
                try: el.update()
                except Exception as e: print(el, 'update error:', e)
    
    def compose(self):
        for element in tuple(self.__elements):
            element.compose()
    
    def draw(self):
        if self.background_color != None:
            # 設定視窗背景顏色
            self.screen.fill(self.background_color)
        for _layer in sorted(self.layers.items(), key=lambda x: x[0]):
            layer = _layer[1]
            for el in layer:
                try:
                    if el.background_color != None:
                        el.image.fill(el.background_color)
                except Exception as e:
                    print(e)
            try:
                layer.draw(self.screen)
            except:
                # 當 Sprite 正在更新時(由於子線程所觸發)，將會導致繪製失敗
                # 繪製失敗會導致程序崩潰，為了預防崩潰，嘗試逐一繪製 Sprite。
                for el in layer:
                    try: self.screen.blit(el.image, el.rect, None, 0)
                    except: pass

    def kill(self):
        for element in tuple(self.all_elements):
            element.kill()
        if controller.current_scene is self:
            controller.current_scene = None
    
    def reload(self):
        is_current_scene = self is controller.current_scene
        controller.unload_sceen(self)
        if is_current_scene:
            controller.goto_scene(self)

    def play(self):
        self.update()
        self.compose()
        self.draw()

from components.controller import controller
from components.scenes.main_menu import main_menu
from components.scenes.pause_menu import pause_menu
from components.scenes.main_game import main_game
from components.scenes.the_end import the_end

class SceneCollection:
    main_menu = main_menu
    pause_menu = pause_menu
    main_game = main_game
    the_end = the_end

scenes = SceneCollection()
