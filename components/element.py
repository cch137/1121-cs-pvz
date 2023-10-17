from typing import *
import pygame
from components.events import *
from components.scene import Scene

ROW = 'row'
COLUMN = 'column'
BLOCK = 'block'
DISPLAY_MODES = (ROW, COLUMN, BLOCK)

CENTER = 'center'
START = 'start'
END = 'end'

class Element(pygame.sprite.Sprite):
    pass

class Element(pygame.sprite.Sprite):
    computed_width: int
    computed_height: int
    parent: Element | None
    scene: Scene | None

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
    def coor(self):
        return self.rect.topleft

    @coor.setter
    def coor(self, value: Tuple[int,int]):
        self.rect.topleft = value

    @property
    def computed_width(self) -> int:
        if self.display == ROW:
            children = self.children
            return sum(child.computed_width for child in children) \
                + self.spacing * (len(children) - 1) \
                + self.padding_left + self.padding_right
        elif self.display == COLUMN:
            return max(child.computed_width for child in self.children) \
                + self.padding_left + self.padding_right
        return self.rect.width

    @property
    def computed_height(self) -> int:
        if self.display == ROW:
            return max(child.computed_height for child in self.children) \
                + self.padding_top + self.padding_bottom
        elif self.display == COLUMN:
            children = self.children
            return sum(child.computed_height for child in self.children) \
                + self.spacing * (len(children) - 1) \
                + self.padding_top + self.padding_bottom
        return self.rect.height

    __display = BLOCK

    background_color: str = None

    @property
    def display(self):
        return self.__display

    @display.setter
    def display(self, value: str):
        if value not in DISPLAY_MODES:
            raise 'Invalid Element display mode'
        self.__display = value
    
    @display.deleter
    def display(self):
        raise 'Element.mode cannot be deleted'

    '''Space between child elements.'''
    spacing: int = 0

    __paddings: list[int] = [0, 0, 0, 0]
    '''Paddings (top, right, bottom, left)'''

    @property
    def padding(self):
        '''Padding between self and child elements.'''
        return sum(self.__paddings) / 4

    @padding.setter
    def padding(self, value: int):
        self.__paddings = [value] * 4

    @property
    def padding_top(self):
        return self.__paddings[0]
    
    @padding_top.setter
    def padding_top(self, value: int):
        self.__paddings[0] = value

    @property
    def padding_bottom(self):
        return self.__paddings[2]
    
    @padding_bottom.setter
    def padding_bottom(self, value: int):
        self.__paddings[2] = value

    @property
    def padding_left(self):
        return self.__paddings[3]
    
    @padding_left.setter
    def padding_left(self, value: int):
        self.__paddings[3] = value

    @property
    def padding_right(self):
        return self.__paddings[1]
    
    @padding_right.setter
    def padding_right(self, value: int):
        self.__paddings[1] = value
    
    @property
    def padding_x(self):
        return (self.__paddings[1] + self.__paddings[3]) / 2
    
    @padding_x.setter
    def padding_x(self, value: int):
        self.__paddings[1] = value
        self.__paddings[3] = value

    @property
    def padding_y(self):
        return (self.__paddings[0] + self.__paddings[2]) / 2

    @padding_y.setter
    def padding_y(self, value: int):
        self.__paddings[0] = value
        self.__paddings[2] = value

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
        watched = {}
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

    _scene: Scene = None
    @property
    def scene(self):
        if self._scene is None:
            if self.parent is None:
                return None
            return self.parent.scene
        return self._scene

    @scene.setter
    def scene(self, value: Scene):
        if self.parent is None:
            self._scene = value
        else:
            self.parent.scene = value

class Character(Element):
    def __init__(self, image: pygame.Surface):
        Element.__init__(self, image)

from components.event_manager import event_manager
