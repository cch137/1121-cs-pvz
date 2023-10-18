from typing import *
import pygame
from components.events import *

ROW = 'row'
COLUMN = 'column'
BLOCK = 'block'
INLINE = 'inline'
DISPLAY_MODES = (ROW, COLUMN, BLOCK, INLINE)

CENTER = 'center'
START = 'start'
END = 'end'

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

class Element(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface | Tuple[int,int] = (0, 0), children: List[Element] = []):
        pygame.sprite.Sprite.__init__(self)
        if type(image) == pygame.Surface:
            self.image = image
        elif type(image) == tuple:
            if type(image[0]) == int and type(image[1]) == int:
                self.image = pygame.Surface((image[0], image[1]))
        else:
            raise 'Invalid image'
        self.rect = self.image.get_rect()
        if children.__len__():
            self.__children = [child for child in children]

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
        return self.display in (BLOCK, INLINE) and len(self.children) == 0

    @property
    def content_width(self) -> int:
        if self.display == ROW or self.__is_end_element:
            children = self.children
            return sum(child.computed_width for child in children) \
                + self.spacing * (len(children) - 1)
        elif self.display == COLUMN or self.__is_end_element:
            return max(child.computed_width for child in self.children)
        return self.width

    @property
    def content_height(self) -> int:
        if self.display == ROW or self.__is_end_element:
            return max(child.computed_height for child in self.children)
        elif self.display == COLUMN or self.__is_end_element:
            children = self.children
            return sum(child.computed_height for child in self.children) \
                + self.spacing * (len(children) - 1)
        return self.height

    @property
    def computed_width(self) -> int:
        value = self.content_width + self.padding_left + self.padding_right
        if self.min_width != None and value < self.min_width:
            return self.min_width
        if self.max_width != None and value > self.max_width:
            return self.max_width
        return value

    @property
    def computed_height(self) -> int:
        value = self.content_height + self.padding_top + self.padding_bottom
        if self.min_height != None and value < self.min_height:
            return self.min_height
        if self.max_height != None and value > self.max_height:
            return self.max_height
        return value

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
        '''排版不考慮 max_..., min_... 屬性'''
        self.width = self.computed_width
        self.height = self.computed_height
        align_items = self.align_items
        justify_content = self.justify_content
        if self.display in (ROW, INLINE):
            # 設定 x 座標
            if justify_content == START:
                x = self.padding_left
                for child in self.children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            elif justify_content == END:
                x = self.padding_right
                for child in reversed(self.children):
                    child.rect.right = x
                    x += child.computed_width + self.spacing
            else:
                x = self.content_width / 2
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
                x = self.rect.centery
                for child in self.children:
                    child.rect.centerx = x
            # 設定 y 座標
            if align_items == START:
                y = self.padding_top
                for child in self.children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
            elif align_items == END:
                y = self.padding_bottom
                for child in reversed(self.children):
                    child.rect.bottom = y
                    y += child.computed_height + self.spacing
            else:
                y = self.content_height / 2
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
            parents.append(ele)
            ele = self.parent
        return parents
    
    @property
    def z_index(self) -> int:
        return self.parents.__len__()

    __children: List[Element] = []

    @property
    def children(self):
        return self.__children.copy()

    def append_child(self, *children: Element):
        for child in children:
            if child in self.__children:
                self.remove_child(child)
            self.__children.append(child)
            child.parent = self

    def remove_child(self, *children: Element):
        for child in children:
            if child in self.__children:
                self.__children.remove(child)
                child.parent = None
    
    def insert_child(self, index: int, *children: Element):
        children = tuple(reversed(children))
        for child in children:
            if child in self.__children:
                self.remove_child(child)
            self.__children.insert(index, child)
            child.parent = self
    
    def insert_before(self, node: Element, *children: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node)
        children = tuple(reversed(children))
        for child in children:
            self.insert_child(index, child)
    
    def insert_after(self, node: Element, child: Element):
        if node not in self.__children: raise 'node is not in children'
        index = self.__children.index(node) + 1
        children = tuple(reversed(children))
        for child in children:
            self.insert_child(index, child)

    @property
    def all_children(self) -> Set[Element]:
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
        return children

class Character(Element):
    def __init__(self, image: pygame.Surface):
        Element.__init__(self, image)

from components.event_manager import event_manager
