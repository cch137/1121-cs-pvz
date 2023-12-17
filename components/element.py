from typing import *
from utils.constants import *
import utils.process as process
from utils.refs import Ref, is_ref, to_ref, to_value
import pygame
from pygame.transform import scale
import math

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
    __cache_manager_dict: Dict[str, CacheItem] = {}

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

from components.events import *
import components.scenes as scenes

_FLYOUT = 'flyout'

class Element(pygame.sprite.Sprite, EventTarget):
    __children: List[Element]

    scene: scenes.Scene | None = None
    parent: Element | None = None
    '''`.parent` is a READ ONLY property, please do not modify it.'''

    display: DisplayValue = BLOCK

    background_color: ColorValue = None

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

    justify_content: AlignValue = CENTER
    '''Horizontal alignment.
    
    水平排列，e.g. 靠左、居中、靠右'''

    align_items: AlignValue = CENTER
    '''Vertical alignment.
    
    縱向排列，e.g. 靠上、居中、靠下'''

    @property
    def children(self):
        return tuple(self.__children)

    def __init__(self, image: pygame.Surface | Coordinate | None = None, display: DisplayValue = None, children: Iterable[Element] = []):
        '''使用大小創建 Element 會將該大小設為此 Element 的 min_width 和 min_height'''
        pygame.sprite.Sprite.__init__(self)
        self.__attributes: Dict[str, Any] = dict()
        if image is None:
            image = (0, 0)
        elif isinstance(image, int):
            image = (image, image)
        if isinstance(image, (tuple, Sequence, pygame.math.Vector2)):
            if len(image) < 2: image = (image[0], 0)
            self.image = pygame.Surface(image)
            self.min_width, self.min_height = image
        elif isinstance(image, pygame.Surface):
            self.image = image
        self.display = display or BLOCK
        self.__children = list()
        self.caches = CacheManager()
        self.append_child(*children)

    def get_attribute(self, name: str):
        return self.__attributes.get(name)

    def set_attribute(self, name: str, value: Any = None):
        self.__attributes[name] = value

    def remove_attribute(self, name: str):
        del self.__attributes[name]
    
    def has_attribute(self, name: str):
        return name in self.__attributes

    radius_scale = 0.5

    def point_in_radius(self, x: float, y: float):
        return math.dist((x, y), self.rect.center) < self.radius

    @property
    def image(self) -> pygame.Surface:
        return self.get_attribute('image')
    
    @image.setter
    def image(self, value: pygame.Surface):
        if not (value.get_flags() & pygame.SRCALPHA):
            value = value.convert_alpha()
        self.set_attribute('image', value)
        center = self.rect.center if hasattr(self, 'rect') and self.rect is not None else None
        self.rect = value.get_rect()
        if center: self.rect.center = center

    @property
    def radius(self) -> int:
        return (min(self.rect.width, self.rect.height) / 2) * self.radius_scale

    @property
    def cursor(self) -> CursorValue:
        return self.get_attribute(CURSOR)

    @cursor.setter
    def cursor(self, value: CursorValue):
        if value is None:
            self.remove_event_listener(CURSOR)
            return
        self.set_attribute(CURSOR, value)
        self.add_event_listener(CURSOR)

    @property
    def cursor_r(self) -> CursorValue:
        return self.get_attribute(CURSOR_R)

    @cursor_r.setter
    def cursor_r(self, value: CursorValue):
        if value is None:
            self.remove_event_listener(CURSOR_R)
            return
        self.set_attribute(CURSOR_R, value)
        self.add_event_listener(CURSOR_R)

    @property
    def allow_flyout(self):
        '''如果把 allow_flyout 設為 False 那麼此元素離開視窗可視範圍時會自動被銷毀(kill)'''
        return not self.has_attribute(_FLYOUT)

    @allow_flyout.setter
    def allow_flyout(self, value: bool):
        if value:
            self.remove_event_listener(_FLYOUT)
            return
        self.set_attribute(_FLYOUT, False)
        self.add_event_listener(_FLYOUT)

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
    def is_end_element(self):
        '''是否為末端的元素'''
        return len(self) == 0

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
        w = self.computed_width
        h = self.computed_height
        if self.width != w or self.height != h:
            self.image = scale(self.image, (w, h))
        rect = self.rect
        align_items = self.align_items
        justify_content = self.justify_content
        if self.display in (ROW, INLINE):
            # 設定 x 座標
            if justify_content == START:
                x = rect.left + self.padding_left
                for child in self.__children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            elif justify_content == END:
                x = rect.right - self.padding_right
                for child in reversed(self.__children):
                    child.rect.right = x
                    x -= child.computed_width + self.spacing
            else:
                x = rect.left + self.padding_left \
                    + (self.computed_width - self.padding_left - self.padding_right) / 2 \
                    - (self.content_width / 2)
                for child in self.__children:
                    child.rect.left = x
                    x += child.computed_width + self.spacing
            # 設定 y 座標
            if align_items == START:
                y = rect.top + self.padding_top
                for child in self.__children:
                    child.rect.top = y
            elif align_items == END:
                y = rect.bottom - self.padding_bottom
                for child in self.__children:
                    child.rect.bottom = y
            else:
                y = rect.centery
                for child in self.__children:
                    child.rect.centery = y
        else: # display in (COLUMN, BLOCK, default)
            # 設定 x 座標
            if justify_content == START:
                x = rect.left + self.padding_left
                for child in self.__children:
                    child.rect.left = x
            elif justify_content == END:
                x = rect.right - self.padding_right
                for child in self.__children:
                    child.rect.right = x
            else:
                x = rect.centerx
                for child in self.__children:
                    child.rect.centerx = x
            # 設定 y 座標
            if align_items == START:
                y = rect.top + self.padding_top
                for child in self.__children:
                    child.rect.top = y
                    y += child.computed_height + self.spacing
            elif align_items == END:
                y = rect.bottom - self.padding_bottom
                for child in reversed(self.__children):
                    child.rect.bottom = y
                    y -= child.computed_height + self.spacing
            else:
                y = rect.top + self.padding_top \
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
        return (self.padding_top, self.padding_right, self.padding_bottom, self.padding_left)

    @padding.setter
    def padding(self, value: int | Tuple[int]):
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
        scene = self.scene
        if scene:
            scene.disconnect_element(self)
        self.set_attribute('z_index', value)
        if scene:
            scene.connect_element(self)

    def index(self, child: Element):
        '''Returns the index of the child'''
        return self.__children.index(child)

    def append_child(self, *children: Element):
        '''Appends elements to the end of the children of this element.'''
        self.remove_child(*children)
        self.__children.extend(children)
        for child in children:
            child.parent = self
            child.connect_scene(self.scene)

    def remove_child(self, *children: Element):
        '''Remove elements from children of this element.'''
        for child in children:
            if child in self.__children:
                self.__children.remove(child)
                child.parent = None
                child.disconnect_scene()

    def insert_child(self, index: int, *children: Element):
        '''Insert elements into children of this element at the given index.'''
        self.remove_child(*children)
        for child in tuple(reversed(children)):
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
        for child in tuple(reversed(children)):
            self.insert_child(index, child)
    
    def insert_after(self, node: Element, *children: Element):
        '''Insert elements into children of this element after the given node(element).'''
        if node not in self.__children:
            raise 'node is not in children'
        index = self.__children.index(node) + 1
        for child in tuple(reversed(children)):
            self.insert_child(index, child)

    @property
    def all_children(self) -> Tuple[Element]:
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
        return tuple(children)

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
        if self.parent:
            self.parent.remove_child(self)
        self.dispatch_event(KillEvent(self))
        self.remove_all_event_listeners()
        self.disconnect_scene()
        pygame.sprite.Sprite.kill(self)

class TextBox(Element):
    def __init__(
            self,
            text: Any | Ref,
            font_size: int = 24,
            font_color: ColorValue = FONT_COLOR,
            font_background: ColorValue | None = None,
            font_name: str = 'assets/fonts/Cubic_11_1.100_R.ttf' or pygame.font.get_default_font(),
            font_antialias: bool = True
            ):
        Element.__init__(self)
        self.ref = to_ref(text)
        self.font_antialias = font_antialias
        self.update_font(font_name, font_size, font_color, font_background)
        self.add_event_listener(REF_CHANGE, lambda: self.update_image())

    def update_font(
            self,
            font_name: str | None = None,
            font_size: int | None = None,
            font_color: ColorValue = None,
            font_background: ColorValue = None
            ):
        if font_name is not None:
            self.__font_name = font_name
        if font_size is not None:
            self.__font_size = font_size
        self.__font_color = font_color
        self.__font_background = font_background
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.update_image()

    def update_image(self, text: str | None = None):
        if text is not None:
            self.ref.value = text
        if self.font is None:
            return
        old_center = self.rect.center
        self.image = self.font.render(self.text, self.font_antialias, self.font_color, self.font_background)
        self.rect.center = old_center

    font: pygame.font.Font | None = None
    __font_name: str = pygame.font.get_default_font()
    __font_size: int = 12
    __font_color: ColorValue | None = None
    __font_background: ColorValue | None = None
    __ref: Ref[Any] | None = None

    @property
    def ref(self):
        return self.__ref

    @ref.setter
    def ref(self, value: Ref[Any]):
        if self.__ref is not None:
            self.__ref.unbind(self)
        self.__ref = value
        value.bind(self)
        self.update_image()

    @property
    def text(self):
        return str(self.ref.value)

    @text.setter
    def text(self, value: Any):
        self.update_image(str(value))

    @property
    def font_name(self):
        return self.__font_name

    @font_name.setter
    def font_name(self, value: str):
        self.update_font(value)

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, value: int):
        self.update_font(None, value)

    @property
    def font_color(self):
        return self.__font_color or FONT_COLOR

    @font_color.setter
    def font_color(self, value: ColorValue):
        self.update_font(None, None, value)

    @property
    def font_background(self):
        return self.__font_background

    @font_background.setter
    def font_background(self, value: ColorValue):
        self.update_font(None, None, None, value)

class EventHandler():
    def __init__(self) -> None:
        self.__target_sets: Dict[str, Set[Element]] = dict()

    def get_targets(self, eventName: str, writable: bool = False):
        if writable:
            return self.__target_sets.setdefault(eventName, set())
        else:
            return tuple(self.__target_sets.setdefault(eventName, set()))

    def get_playing_targets(self, *eventNames: str):
        return tuple(el for els in tuple(self.get_targets(eventName) for eventName in eventNames) for el in els if el.is_playing)

    def add_target(self, target: Element, eventName: str):
        self.get_targets(eventName, True).add(target)

    def remove_target(self, target: Element, eventName: str):
        self.get_targets(eventName, True).remove(target)

    def dispatch_basic_events(self):
        from components import controller

        pos = pygame.mouse.get_pos()
        x, y = pos

        # dispatch HoverEvent
        for el in self.get_playing_targets(HOVER):
            if el.rect.collidepoint(x, y):
                el.dispatch_event(HoverEvent(pos, el))
        for el in self.get_playing_targets(HOVER_R):
            if el.point_in_radius(x, y):
                el.dispatch_event(HoverREvent(pos, el))

        # dispatch MouseEnterEvent and MouseLeaveEvent
        for el in self.get_playing_targets(MOUSEENTER, MOUSELEAVE):
            if el.rect.collidepoint(x, y):
                if not el.has_attribute(HOVER):
                    el.dispatch_event(MouseEnterEvent(pos, el))
                    el.set_attribute(HOVER, True)
            elif el.has_attribute(HOVER):
                el.remove_attribute(HOVER)
                el.dispatch_event(MouseLeaveEvent(pos, el))
        for el in self.get_playing_targets(MOUSEENTER_R, MOUSELEAVE_R):
            if el.point_in_radius(x, y):
                if not el.has_attribute(HOVER_R):
                    el.dispatch_event(MouseEnterREvent(pos, el))
                    el.set_attribute(HOVER_R, True)
            elif el.has_attribute(HOVER_R):
                el.remove_attribute(HOVER_R)
                el.dispatch_event(MouseLeaveREvent(pos, el))
        
        # detect _FLYOUT
        screen_rect = controller.screen_rect
        screen_right = screen_rect.right
        screen_left = screen_rect.left
        screen_bottom = screen_rect.bottom
        screen_top = screen_rect.top
        for el in self.get_playing_targets(_FLYOUT):
            rect = el.rect
            if rect.left > screen_right or rect.right < screen_left\
            or rect.top > screen_bottom or rect.bottom < screen_top:
                el.kill()

        # detect cursor style
        for el in reversed(sorted(self.get_playing_targets(CURSOR_R), key=lambda x: x.z_index)):
            if not el.point_in_radius(x, y):
                continue
            match el.cursor_r:
                case 'arrow':
                    controller.cursor.arrow()
                case 'crosshair':
                    controller.cursor.crosshair()
                case 'hand':
                    controller.cursor.hand()
                case 'ibeam':
                    controller.cursor.ibeam()
                case 'sizeall':
                    controller.cursor.sizeall()
                case _:
                    if isinstance(el.cursor_r, int):
                        controller.cursor.set(el.cursor_r)
                    else:
                        controller.cursor.default()
            return
        for el in reversed(sorted(self.get_playing_targets(CURSOR), key=lambda x: x.z_index)):
            if not el.rect.collidepoint(x, y):
                continue
            match el.cursor:
                case 'arrow':
                    controller.cursor.arrow()
                case 'crosshair':
                    controller.cursor.crosshair()
                case 'hand':
                    controller.cursor.hand()
                case 'ibeam':
                    controller.cursor.ibeam()
                case 'sizeall':
                    controller.cursor.sizeall()
                case _:
                    if isinstance(el.cursor, int):
                        controller.cursor.set(el.cursor)
                    else:
                        controller.cursor.default()
            return
        controller.cursor.default()

    def handle(self, event: pygame.event.Event):
        now = process.timestamp

        # dispatch ClickEvent
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for el in self.get_playing_targets(CLICK, CLICK_R):
                    if el.rect.collidepoint(x, y):
                        el.set_attribute(BUTTONDOWN, (event.button, now))
                    if el.point_in_radius(x, y):
                        el.set_attribute(BUTTONDOWN_R, (event.button, now))
            case pygame.MOUSEBUTTONUP:
                x, y = event.pos
                # mousedown 與 mouseup 之間的間隔在 1 秒內，且按下的按鍵相同，就會被判定為 click 事件
                for el in self.get_playing_targets(CLICK):
                    if el.has_attribute(BUTTONDOWN):
                        button, mousedown_at = el.get_attribute(BUTTONDOWN)
                        if el.rect.collidepoint(x, y) \
                            and button == event.button \
                            and now - mousedown_at < 1:
                            if event.button == pygame.BUTTON_LEFT:
                                el.dispatch_event(ClickEvent(event.pos, el))
                        el.remove_attribute(BUTTONDOWN)
                # click in radius 的判斷與 click 相同
                for el in self.get_playing_targets(CLICK_R):
                    if el.has_attribute(BUTTONDOWN_R):
                        button, mousedown_at = el.get_attribute(BUTTONDOWN_R)
                        if el.point_in_radius(x, y) \
                            and button == event.button \
                            and now - mousedown_at < 1:
                            if event.button == pygame.BUTTON_LEFT:
                                el.dispatch_event(ClickREvent(event.pos, el))
                        el.remove_attribute(BUTTONDOWN_R)
            case pygame.KEYDOWN:
                for el in self.get_playing_targets(KEYDOWN):
                    el.dispatch_event(KeydownEvent(event.key, el))

event_handler = EventHandler()
