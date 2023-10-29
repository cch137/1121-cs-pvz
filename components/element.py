from typing import *
from constants import *
import utils.process as process
from utils.elong import elong
import pygame
import os

def load_image(filepath: str, size: Tuple[int,int] = None):
    image = pygame.image.load(os.path.join('assets', *filepath.replace('\\', '/').split('/')))
    if size is None:
        return image
    return pygame.transform.scale(image, size)

def load_animation(filepath: str, frames: int, duration_sec: float, size: Tuple[int,int] = None):
    '''動畫圖片命名格式例子：anim_1.png, anim_2.png, ..., anim_10.png （假設圖片放置在 assets 目錄）
    
    函式使用例子：load_animation('assets/anim', 10, 1.5, (60, 60))'''
    return elong(
        [load_image(f'{filepath}_{i}.png', size) for i in range(1, frames + 1)],
        round(duration_sec * FPS)
    )

def create_textbox(
        text: str,
        size: int = 12,
        color: tuple[int,int,int] = FONT_COLOR,
        background: tuple[int,int,int] | None = None,
        font_name: str = pygame.font.get_default_font()
    ):
    font = pygame.font.Font(font_name, size)
    return font.render(text, True, color, background)

class Element(pygame.sprite.Sprite):
    pass

class Element(pygame.sprite.Sprite):
    rect: pygame.Rect
    x: int
    y: int
    computed_width: int
    computed_height: int
    parent: Element | None
    parents: List[Element]
    z_index: int
    compose: Callable

class CacheItem():
    def __init__(self, value: Any = None):
        self.__value = value
        self.ticks = process.ticks
    
    @property
    def is_valid(self):
        return self.ticks == process.ticks

    def get(self):
        if self.is_valid:
            return self.__value
        return None

    def set(self, value: Any):
        self.__value = value
        self.ticks = process.ticks
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

import components.events as events
import components.scenes as scenes

class Element(pygame.sprite.Sprite, events.EventTarget):
    __children: List[Element]

    scene: scenes.Scene | None = None
    parent: Element | None = None
    '''`.parent` is a READ ONLY property, please do not modify it.'''

    display: Literal['block', 'inline', 'row', 'column'] = BLOCK

    background_color: tuple[int] = None

    min_width: int | None = None
    max_width: int | None = None
    min_height: int | None = None
    max_height: int | None = None

    padding_top = 0
    padding_bottom = 0
    padding_left = 0
    padding_right = 0

    spacing: int = 0
    '''The spacing between child elements.'''

    justify_content: Literal['start','center','end'] = CENTER
    '''Horizontal alignment.
    
    水平排列，e.g. 靠左、居中、靠右'''

    align_items: Literal['start','center','end'] = CENTER
    '''Vertical alignment.
    
    縱向排列，e.g. 靠上、居中、靠下'''

    @property
    def children(self):
        return list(self.__children)

    def __init__(self, image: pygame.Surface | Tuple[int,int] | None = None, display: Literal['block', 'inline', 'row', 'column'] | None = None, children: Iterable[Element] = []):
        '''使用大小創建 Element 會將該大小設為此 Element 的 min_width 和 min_height'''
        pygame.sprite.Sprite.__init__(self)
        events.EventTarget.__init__(self)
        if image is None:
            image = (0, 0)
        elif isinstance(image, int):
            image = (image, image)
        if isinstance(image, tuple):
            if len(image) < 2: image = (image[0], 0)
            self.image = pygame.Surface(image)
            self.min_width, self.min_height = image
        elif isinstance(image, pygame.Surface):
            self.image = image
        self.display = display or BLOCK
        self.__children = list()
        self.caches = CacheManager()
        self.append_child(*children)

    radius_scale = 0.5

    @property
    def image(self) -> pygame.Surface:
        return self.get_attribute('image')
    
    @image.setter
    def image(self, value: pygame.Surface):
        self.set_attribute('image', value)
        self.rect = value.get_rect()

    @property
    def radius(self) -> int:
        return (min(self.rect.width, self.rect.height) / 2) * self.radius_scale

    @property
    def cursor(self) -> int:
        return self.get_attribute(events.CURSOR)

    @cursor.setter
    def cursor(self, value: None | int | Literal['arrow','crosshair','hand','ibeam','sizeall','default']):
        if value is None:
            self.remove_event_listener(events.CURSOR)
            return
        self.set_attribute(events.CURSOR, value)
        self.add_event_listener(events.CURSOR)

    @property
    def allow_flyout(self):
        '''如果把 allow_flyout 設為 False 那麼此元素離開視窗可視範圍時會自動被銷毀(kill)'''
        return not self.has_attribute(events._FLYOUT)

    @allow_flyout.setter
    def allow_flyout(self, value: bool):
        if value:
            self.remove_event_listener(events._FLYOUT)
            return
        self.set_attribute(events._FLYOUT, False)
        self.add_event_listener(events._FLYOUT)

    def __len__(self):
        return self.__children.__len__()

    @property
    def is_playing(self):
        if self.scene is None:
            return False
        return self.scene.is_playing

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
    def is_end_element(self):
        '''是否為末端的元素'''
        return self.display in (BLOCK, INLINE) and len(self) == 0

    @property
    def content_width(self) -> int:
        cache = self.caches.get('content_w')
        if cache is not None:
            return cache
        if self.is_end_element:
            return_value = self.width
        else:
            if self.display in (ROW, INLINE):
                return_value = sum(child.computed_width for child in self.__children) \
                    + self.spacing * (len(self) - 1)
            else:
                return_value = max(child.computed_width for child in self.__children)
        return self.caches.set('content_w', return_value)

    @property
    def content_height(self) -> int:
        cache = self.caches.get('content_h')
        if cache is not None:
            return cache
        if self.is_end_element:
            return_value = self.height
        else:
            if self.display in (ROW, INLINE):
                return_value = max(child.computed_height for child in self.__children)
            else:
                return_value = sum(child.computed_height for child in self.__children) \
                    + self.spacing * (len(self) - 1)
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
        '''Layouts (positions) itself and all child elements, but does not draw them.

        排版不進行繪製。此方法也同時對所有層級的子元素作用。'''
        self.width = self.computed_width
        self.height = self.computed_height
        align_items = self.align_items
        justify_content = self.justify_content
        if self.display in (ROW, INLINE):
            # 設定 x 座標
            if justify_content == START:
                x = self.rect.left + self.padding_left
                for child in self.__children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            elif justify_content == END:
                x = self.rect.right - self.padding_right
                for child in reversed(self.__children):
                    child.rect.right = x
                    x -= child.computed_width + self.spacing
            else:
                x = self.rect.left + self.padding_left \
                    + (self.computed_width - self.padding_left - self.padding_right) / 2 \
                    - (self.content_width / 2)
                for child in self.__children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            # 設定 y 座標
            if align_items == START:
                y = self.padding_top
                for child in self.__children:
                    child.rect.top = y
            elif align_items == END:
                y = self.padding_bottom
                for child in self.__children:
                    child.rect.bottom = y
            else:
                y = self.rect.centery
                for child in self.__children:
                    child.rect.centery = y
        else: # display in (COLUMN, BLOCK, default)
            # 設定 x 座標
            if justify_content == START:
                x = self.padding_left
                for child in self.__children:
                    child.rect.left = x
            elif justify_content == END:
                x = self.padding_right
                for child in self.__children:
                    child.rect.right = x
            else:
                x = self.rect.centerx
                for child in self.__children:
                    child.rect.centerx = x
            # 設定 y 座標
            if align_items == START:
                y = self.rect.top + self.padding_top
                for child in self.__children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
            elif align_items == END:
                y = self.rect.bottom - self.padding_bottom
                for child in reversed(self.__children):
                    child.rect.bottom = y
                    y -= child.computed_height + self.spacing
            else:
                y = self.rect.top + self.padding_top \
                    + (self.computed_height - self.padding_top - self.padding_bottom) / 2 \
                    - (self.content_height / 2)
                for child in self.__children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
        for child in self.__children:
            child.compose()

    @property
    def padding(self):
        '''The spacing between this element's edge and its children.'''
        return (self.padding_top + self.padding_bottom + self.padding_left + self.padding_right) / 4

    @padding.setter
    def padding(self, value: int | tuple[int]):
        if not isinstance(value, tuple):
            value = (value,)
        self.padding_top = value[0]
        match len(value):
            case 1:
                self.padding_right = value[0]
                self.padding_bottom = value[0]
                self.padding_left = value[0]
            case 2:
                self.padding_right = value[1]
                self.padding_bottom = value[0]
                self.padding_left = value[1]
            case 3:
                self.padding_right = value[1]
                self.padding_bottom = value[2]
                self.padding_left = value[1]
            case _:
                self.padding_right = value[1]
                self.padding_bottom = value[2]
                self.padding_left = value[3]

    @property
    def parents(self) -> List[Element]:
        '''All parent elements of this element.'''
        if self.parent is None:
            return []
        return self.parent.parents + [self.parent]

    @property
    def z_index(self) -> int:
        if self.has_attribute('z_index'):
            return self.get_attribute('z_index')
        if self.parent is None:
            return 0
        return self.parent.z_index + 1

    @z_index.setter
    def z_index(self, value: int | None):
        self.set_attribute('z_index', value)

    def index(self, child: Element):
        '''Returns the index of the child'''
        return self.__children.index(child)

    def append_child(self, *children: Element):
        '''Appends elements to the end of the children of this element.'''
        self.remove_child(*children)
        self.__children.extend(children)
        for child in list(children):
            child.parent = self
            child.connect_scene(self.scene)

    def remove_child(self, *children: Element):
        '''Remove elements from children of this element.'''
        for child in list(children):
            if child in self.__children:
                self.__children.remove(child)
                child.parent = None
                child.disconnect_scene()

    def insert_child(self, index: int, *children: Element):
        '''Insert elements into children of this element at the given index.'''
        self.remove_child(*children)
        children = list(reversed(list(children)))
        for child in children:
            self.__children.insert(index, child)
            child.parent = self
            child.connect_scene(self.scene)
    
    def move_child(self, new_parent: Element, *children):
        '''Move child elements from this element to another element.'''
        self.remove_child(child for child in children)
        new_parent.append_child(child for child in children)
    
    def insert_before(self, node: Element, *children: Element):
        '''Insert elements into children of this element before the given node(element).'''
        if node not in self.__children:
            raise 'node is not in children'
        index = self.__children.index(node)
        children = list(reversed(list(children)))
        for child in children:
            self.insert_child(index, child)
    
    def insert_after(self, node: Element, child: Element):
        '''Insert elements into children of this element after the given node(element).'''
        if node not in self.__children:
            raise 'node is not in children'
        index = self.__children.index(node) + 1
        children = list(reversed(list(children)))
        for child in children:
            self.insert_child(index, child)

    @property
    def all_children(self) -> List[Element]:
        '''All hierarchical child elements below this element.

        在此元素之下所有層級的子元素。'''
        watched = set()
        parents = { self }
        children = set()
        while len(watched) != len(parents):
            for parent in tuple(parents):
                if parent in watched:
                    continue
                for child in parent.children:
                    children.add(child)
                    parents.add(child)
                watched.add(parent)
        return list(children)

    def connect_scene(self, scene: scenes.Scene | None):
        '''Connect with the scene. (draw and update this element in the scene)

        注：此方法僅在 scene 內和 self 內更動 children 時調用。此方法也同時對所有層級的子元素作用。'''
        if scene is None: return
        scene.connect_element(self)
        self.scene = scene
        for child in self.__children:
            child.connect_scene(scene)

    def disconnect_scene(self):
        '''Disconnect with the scene.

        注：此方法僅在 scene 內和 self 內更動 children 時調用。此方法也同時對所有層級的子元素作用。'''
        if self.scene is None: return
        self.scene.disconnect_element(self)
        self.scene = None
        for child in self.__children:
            child.disconnect_scene()
    
    def kill(self):
        '''Remove the Element from all Groups. Remove all event listeners of the Element.'''
        self.remove_all_event_listeners()
        self.disconnect_scene()
        pygame.sprite.Sprite.kill(self)
