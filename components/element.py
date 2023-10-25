from typing import *
import utils.process as process
import pygame
import random

class Element(pygame.sprite.Sprite):
    pass

class Element(pygame.sprite.Sprite):
    rect: pygame.Rect
    x: int
    y: int
    computed_width: int
    computed_height: int
    parent: Element | None
    compose: Callable

from components.events import *
from components.scene import Scene

ROW = 'row'
COLUMN = 'column'
BLOCK = 'block'
INLINE = 'inline'
DISPLAY_MODES = (ROW, COLUMN, BLOCK, INLINE)

CENTER = 'center'
START = 'start'
END = 'end'

class CacheItem():
    def __init__(self, value: Any = None):
        self.__value = value
        self.timestamp = process.timestamp
    
    @property
    def is_valid(self):
        return self.timestamp == process.timestamp

    def get(self):
        if self.is_valid:
            return self.__value
        return None

    def set(self, value: Any):
        self.__value = value
        self.timestamp = process.timestamp
        return value

class CacheManager():
    __cache_manager_dict: dict[str, CacheItem] = {}

    def create(self, key: str, value: Any = None):
        cache = CacheItem(value)
        self.__cache_manager_dict[key] = cache
        return cache

    def get_cache_item(self, key: str):
        return self.__cache_manager_dict.get(key, self.create(key))

    def get(self, key: str):
        return self.get_cache_item(key).get()

    def set(self, key: str, value: Any):
        return self.get_cache_item(key).set(value)

class EventTarget():
    __listeners: dict[str, set[Callable]] = {}

    def add_event_listener(self, eventName: str, listener: Callable):
        if eventName not in self.__listeners:
            self.__listeners[eventName] = set()
        self.__listeners[eventName].add(listener)
        event_manager.add_element(self, eventName)

    def remove_event_listener(self, eventName: str, listener: Callable):
        if eventName not in self.__listeners: return
        if listener not in self.__listeners[eventName]: return
        self.__listeners[eventName].remove(listener)
        if self.__listeners[eventName].__len__() == 0:
            event_manager.remove_element(self, eventName)

    def dispatch_event(self, event: UserEvent):
        if event.name in self.__listeners:
            for listener in self.__listeners[event.name]:
                try:
                    if listener.__code__.co_argcount > 0: listener(event)
                    else: listener()
                except Exception as err:
                    print(err)

    __attributes = {}

    def get_attribute(self, name: str):
        return self.__attributes.get(name)

    def set_attribute(self, name: str, value):
        self.__attributes[name] = value

    def remove_attribute(self, name: str):
        del self.__attributes[name]
    
    def has_attribute(self, name: str):
        return name in self.__attributes

class Element(pygame.sprite.Sprite, EventTarget):
    def __init__(self, image: pygame.Surface | Tuple[int,int] = (0, 0), display: Literal['block', 'inline', 'row', 'column'] = BLOCK, children: List[Element] = []):
        pygame.sprite.Sprite.__init__(self)
        EventTarget.__init__(self)
        if type(image) == pygame.Surface:
            self.image = image
        elif type(image) == tuple:
            w, h = image
            self.image = pygame.Surface(image)
            if display in (COLUMN, ROW):
                self.min_width = w
                self.min_height = h
        else:
            raise 'Invalid image'
        self.display = display
        self.rect = self.image.get_rect()
        self.__children = list()
        self.scenes = set()
        self.caches = CacheManager()
        if children.__len__():
            self.__children = [child for child in children]
    
    @property
    def id(self) -> str | None:
        return self.get_attribute('id')

    @id.setter
    def id(self, value: str):
        self.set_attribute('id', value)

    @property
    def x(self): 
        return self.rect.x

    @x.setter
    def x(self, value: int):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value: int):
        self.rect.y = value

    @property
    def __is_end_element(self):
        '''是否為末端的元素'''
        return self.display in (BLOCK, INLINE) and len(self) == 0

    @property
    def content_width(self) -> int:
        cache = self.caches.get('content_w')
        if cache is not None:
            return cache
        if self.__is_end_element:
            return_value = self.width
        else:
            children = self.children
            if self.display in (ROW, INLINE):
                return_value = sum(child.computed_width for child in children) \
                    + self.spacing * (len(children) - 1)
            else:
                return_value = max(child.computed_width for child in children)
        return self.caches.set('content_w', return_value)

    @property
    def content_height(self) -> int:
        cache = self.caches.get('content_h')
        if cache is not None:
            return cache
        if self.__is_end_element:
            return_value = self.height
        else:
            children = self.children
            if self.display in (ROW, INLINE):
                return_value = max(child.computed_height for child in children)
            else:
                return_value = sum(child.computed_height for child in children) \
                    + self.spacing * (len(children) - 1)
        return self.caches.set('content_h', return_value)

    @property
    def computed_width(self) -> int:
        cache = self.caches.get('computed_w')
        if cache is not None:
            return cache
        return_value = self.content_width + self.padding_left + self.padding_right
        if self.min_width != None and return_value < self.min_width:
            return_value = self.min_width
        elif self.max_width != None and return_value > self.max_width:
            return_value = self.max_width
        return self.caches.set('computed_w', return_value)

    @property
    def computed_height(self) -> int:
        cache = self.caches.get('computed_h')
        if cache is not None:
            return cache
        return_value = self.content_height + self.padding_top + self.padding_bottom
        if self.min_height != None and return_value < self.min_height:
            return_value = self.min_height
        elif self.max_height != None and return_value > self.max_height:
            return_value = self.max_height
        return self.caches.set('computed_h', return_value)

    min_width: int | None = None
    max_width: int | None = None

    min_height: int | None = None
    max_height: int | None = None
    
    @property
    def width(self) -> int:
        return self.rect.width
    
    @width.setter
    def width(self, value: int):
        self.rect.width = value
    
    @property
    def height(self) -> int:
        return self.rect.height

    @height.setter
    def height(self, value: int):
        self.rect.height = value

    def compose(self):
        '''排版不考慮 max_..., min_... 屬性，排版不進行繪製。'''
        self.width = self.computed_width
        self.height = self.computed_height
        align_items = self.align_items
        justify_content = self.justify_content
        if self.display in (ROW, INLINE):
            # 設定 x 座標
            if justify_content == START:
                x = self.rect.left + self.padding_left
                for child in self.children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            elif justify_content == END:
                x = self.rect.right - self.padding_right
                for child in reversed(self.children):
                    child.rect.right = x
                    x -= child.computed_width + self.spacing
            else:
                x = self.rect.left + self.padding_left \
                    + (self.computed_width - self.padding_left - self.padding_right) / 2 \
                    - (self.content_width / 2)
                for child in self.children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            # 設定 y 座標
            if align_items == START:
                y = self.padding_top
                for child in self.children:
                    child.rect.top = y
            elif align_items == END:
                y = self.padding_bottom
                for child in self.children:
                    child.rect.bottom = y
            else:
                y = self.rect.centery
                for child in self.children:
                    child.rect.centery = y
        else: # display in (COLUMN, BLOCK, default)
            # 設定 x 座標
            if justify_content == START:
                x = self.padding_left
                for child in self.children:
                    child.rect.left = x
            elif justify_content == END:
                x = self.padding_right
                for child in self.children:
                    child.rect.right = x
            else:
                x = self.rect.centerx
                for child in self.children:
                    child.rect.centerx = x
            # 設定 y 座標
            if align_items == START:
                y = self.rect.top + self.padding_top
                for child in self.children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
            elif align_items == END:
                y = self.rect.bottom - self.padding_bottom
                for child in reversed(self.children):
                    child.rect.bottom = y
                    y -= child.computed_height + self.spacing
            else:
                y = self.rect.top + self.padding_top \
                    + (self.computed_height - self.padding_top - self.padding_bottom) / 2 \
                    - (self.content_height / 2)
                for child in self.children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
        for child in self.children:
            child.compose()

    display: Literal['block', 'inline', 'row', 'column'] = BLOCK

    background_color: str = None

    '''Space between child elements.'''
    spacing: int = 0

    padding_top = 0
    padding_bottom = 0
    padding_left = 0
    padding_right = 0

    @property
    def padding(self):
        '''Padding between self and child elements.'''
        return (self.padding_top + self.padding_bottom + self.padding_left + self.padding_right) / 4

    @padding.setter
    def padding(self, value: int):
        self.padding_x = value
        self.padding_y = value

    @property
    def padding_x(self):
        return (self.padding_left, self.padding_right) / 2

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

    justify_content: Literal['start','center','end'] = CENTER
    '''水平排列，e.g. 靠左、居中、靠右'''

    align_items: Literal['start','center','end'] = CENTER
    '''縱向排列，e.g. 靠上、居中、靠下'''

    parent: Element | None = None

    @property
    def parents(self) -> List[Element]:
        parents = []
        ele = self.parent
        while ele != None:
            if ele in parents:
                break
            parents.append(ele)
            ele = ele.parent
        return parents
    @property
    def z_index(self) -> int:
        return len(self.parents)

    __children: List[Element]

    @property
    def children(self):
        return list(self.__children)

    def __len__(self):
        return self.__children.__len__()

    def append_child(self, *children: Element):
        self.remove_child(*children)
        self.__children.extend(children)
        for child in list(children):
            child.parent = self
            for scene in self.scenes:
                child.connect_scene(scene)

    def remove_child(self, *children: Element):
        for child in list(children):
            if child in self.__children:
                self.__children.remove(child)
                child.parent = None
                for scene in self.scenes:
                    child.disconnect_scene(scene)

    def insert_child(self, index: int, *children: Element):
        self.remove_child(*children)
        children = list(reversed(list(children)))
        for child in children:
            self.__children.insert(index, child)
            child.parent = self
            for scene in self.scenes:
                child.connect_scene(scene)
    
    def move_child(self, new_parent: Element, *children):
        self.remove_child(child for child in children)
        new_parent.append_child(child for child in children)
    
    def insert_before(self, node: Element, *children: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node)
        children = list(reversed(list(children)))
        for child in children:
            self.insert_child(index, child)
    
    def insert_after(self, node: Element, child: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node) + 1
        children = list(reversed(list(children)))
        for child in children:
            self.insert_child(index, child)

    @property
    def all_children(self) -> List[Element]:
        watched = set()
        parents = { self }
        children = set()
        while len(watched) != len(parents):
            for parent in parents:
                if parent in watched:
                    continue
                for child in parent.children:
                    children.add(child)
                    parents.add(child)
                watched.add(parent)
        return list(children)
    
    scenes: set[Scene]

    def connect_scene(self, scene: Scene):
        '''注：此方法也對所有層級的子元素作用。此方法僅在 scene 內和 self 內更動 children 時調用'''
        scene.connect_element(self)
        self.scenes.add(scene)
        children = self.children
        stamp = random.random()
        for child in children:
            child.connect_scene(scene)

    def disconnect_scene(self, scene: Scene):
        '''注：此方法也對所有層級的子元素作用。此方法僅在 scene 內和 self 內更動 children 時調用'''
        scene.disconnect_element(self)
        self.scenes.remove(self)
        for child in self.children:
            child.disconnect_scene(scene)

class Character(Element):
    def __init__(self, image: pygame.Surface):
        Element.__init__(self, image)

from components.event_manager import event_manager
