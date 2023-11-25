'''
這是一個假想中更好的一個 Element 的設計。
未完工。
'''

# class ElementV2(pygame.sprite.Sprite, events.EventTarget): pass

# class Style(events.EventTarget):
#     def __init__(
#             self,
#             display: Attr[DisplayValue] = BLOCK,
#             x: Attr[int | None] = None,
#             y: Attr[int | None] = None,
#             width: Attr[int | None] = None,
#             height: Attr[int | None] = None,
#             min_width: Attr[int | None] = None,
#             max_width: Attr[int | None] = None,
#             min_height: Attr[int | None] = None,
#             max_height: Attr[int | None] = None,
#             background_color: Attr[ColorValue | None] = None,
#             radius_scale: Attr[float] = 0.5,
#             cursor: Attr[CursorValue] = None,
#             cursor_r: Attr[CursorValue] = None,
#             allow_flyout: Attr[bool] = True,
#             spacing: Attr[int] = 0,
#             padding: Attr[int] | None = None,
#             padding_x: Attr[int] | None = None,
#             padding_y: Attr[int] | None = None,
#             padding_top: Attr[int | None] = None,
#             padding_bottom: Attr[int | None] = None,
#             padding_left: Attr[int | None] = None,
#             padding_right: Attr[int | None] = None,
#             justify_content: Attr[AlignValue] = CENTER,
#             align_items: Attr[AlignValue] = CENTER,
#             z_index: Attr[int | None] = None,
#             font_name: Attr[str] = pygame.font.get_default_font(),
#             font_size: Attr[int] = 12,
#             color: Attr[ColorValue | None] = None,
#         ):
#         self.__attributes: Dict[str, Ref[Any] | Any] = dict()
#         self.display = display
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.min_width = min_width
#         self.max_width = max_width
#         self.min_height = min_height
#         self.max_height = max_height
#         self.background_color = background_color
#         self.radius_scale = radius_scale
#         self.cursor = cursor
#         self.cursor_r = cursor_r
#         self.allow_flyout = allow_flyout
#         self.spacing = spacing
#         self.padding_top = ((padding if padding_y is None else padding_y) if padding_top is None else padding_top) or 0
#         self.padding_right = ((padding if padding_x is None else padding_x) if padding_right is None else padding_right) or 0
#         self.padding_bottom = ((padding if padding_y is None else padding_y) if padding_bottom is None else padding_bottom) or 0
#         self.padding_left = ((padding if padding_x is None else padding_x) if padding_left is None else padding_left) or 0
#         self.justify_content = justify_content
#         self.align_items = align_items
#         self.z_index = z_index
#         self.font_size = font_size
#         self.font_name = font_name
#         self.color = color
#         self.__inited = True
    
#     __inited = False

#     def get_attributes(self):
#         return self.__attributes

#     def __getattr(self, name: str, default_value = None):
#         return default_value if name not in self.__attributes else to_value(self.__attributes.get(name))

#     def __setattr(self, name: str, newvalue: Any):
#         if isinstance(newvalue, Ref):
#             self.__attributes[name] = newvalue
#         elif isinstance(self.__attributes.get(name), Ref):
#             self.__attributes[name].value = newvalue
#         else:
#             self.__attributes[name] = newvalue
#         if self.__inited:
#             self.dispatch_event(events.StyleChangeEvent(self, name), None, False)

#     @property
#     def display(self) -> DisplayValue: return self.__getattr('display', BLOCK)
#     @display.setter
#     def display(self, value: DisplayValue): self.__setattr('display', value)

#     @property
#     def x(self) -> int | None: return self.__getattr('x')
#     @x.setter
#     def x(self, value: int | None): self.__setattr('x', value)

#     @property
#     def y(self) -> int | None: return self.__getattr('y')
#     @y.setter
#     def y(self, value: int | None): self.__setattr('y', value)

#     @property
#     def width(self) -> int: return self.__getattr('width')
#     @width.setter
#     def width(self, value: int): self.__setattr('width', value)

#     @property
#     def height(self) -> int: return self.__getattr('height')
#     @height.setter
#     def height(self, value: int): self.__setattr('height', value)

#     @property
#     def min_width(self) -> int | None: return self.__getattr('min_width')
#     @min_width.setter
#     def min_width(self, value: int | None): self.__setattr('min_width', value)

#     @property
#     def max_width(self) -> int | None: return self.__getattr('max_width')
#     @max_width.setter
#     def max_width(self, value: int | None): self.__setattr('max_width', value)

#     @property
#     def min_height(self) -> int | None: return self.__getattr('min_height')
#     @min_height.setter
#     def min_height(self, value: int | None): self.__setattr('min_height', value)

#     @property
#     def max_height(self) -> int | None: return self.__getattr('max_height')
#     @max_height.setter
#     def max_height(self, value: int | None): self.__setattr('max_height', value)

#     @property
#     def background_color(self) -> ColorValue | None: return self.__getattr('background_color')
#     @background_color.setter
#     def background_color(self, value: ColorValue): self.__setattr('background_color', value)

#     @property
#     def radius_scale(self) -> float: return self.__getattr('radius_scale')
#     @radius_scale.setter
#     def radius_scale(self, value: float): self.__setattr('radius_scale', value)

#     @property
#     def cursor(self) -> CursorValue: return self.__getattr('cursor')
#     @cursor.setter
#     def cursor(self, value: CursorValue): self.__setattr('cursor', value)

#     @property
#     def cursor_r(self) -> CursorValue: return self.__getattr('cursor_r')
#     @cursor_r.setter
#     def cursor_r(self, value: CursorValue): self.__setattr('cursor_r', value)

#     @property
#     def allow_flyout(self) -> bool:
#         '''如果把 allow_flyout 設為 False 那麼此元素離開視窗可視範圍時會自動被銷毀(kill)'''
#         return self.__getattr('allow_flyout')
#     @allow_flyout.setter
#     def allow_flyout(self, value: bool): self.__setattr('allow_flyout', value)

#     @property
#     def padding_top(self) -> int: return self.__getattr('padding_top')
#     @padding_top.setter
#     def padding_top(self, value: int): self.__setattr('padding_top', value)

#     @property
#     def padding_right(self) -> int: return self.__getattr('padding_right')
#     @padding_right.setter
#     def padding_right(self, value: int): self.__setattr('padding_right', value)

#     @property
#     def padding_bottom(self) -> int: return self.__getattr('padding_bottom')
#     @padding_bottom.setter
#     def padding_bottom(self, value: int): self.__setattr('padding_bottom', value)

#     @property
#     def padding_left(self) -> int: return self.__getattr('padding_left')
#     @padding_left.setter
#     def padding_left(self, value: int): self.__setattr('padding_left', value)

#     @property
#     def padding_x(self) -> int: return (self.padding_left + self.padding_right) / 2
#     @padding_x.setter
#     def padding_x(self, value: int): self.padding_left = value, self.padding_right = value

#     @property
#     def padding_y(self) -> int: return (self.padding_top + self.padding_bottom) / 2
#     @padding_y.setter
#     def padding_y(self, value: int): self.padding_top = value, self.padding_bottom = value

#     @property
#     def padding(self) -> int:
#         '''The spacing between this element's edge and its children.'''
#         return (self.padding_top + self.padding_bottom + self.padding_left + self.padding_right) / 4
#     @padding.setter
#     def padding(self, value: int | Tuple[int]):
#         if not isinstance(value, tuple):
#             value = (value,)
#         self.padding_top = value[0]
#         match len(value):
#             case 1:
#                 self.padding_right = value[0]
#                 self.padding_bottom = value[0]
#                 self.padding_left = value[0]
#             case 2:
#                 self.padding_right = value[1]
#                 self.padding_bottom = value[0]
#                 self.padding_left = value[1]
#             case 3:
#                 self.padding_right = value[1]
#                 self.padding_bottom = value[2]
#                 self.padding_left = value[1]
#             case _:
#                 self.padding_right = value[1]
#                 self.padding_bottom = value[2]
#                 self.padding_left = value[3]

#     @property
#     def spacing(self) -> int:
#         '''The spacing between child elements.'''
#         return self.__getattr('spacing')
#     @spacing.setter
#     def spacing(self, value: int): self.__setattr('spacing', value)

#     @property
#     def justify_content(self) -> AlignValue:
#         '''Horizontal alignment. 水平排列，e.g. 靠左、居中、靠右'''
#         return self.__getattr('justify_content') or CENTER
#     @justify_content.setter
#     def justify_content(self, value: AlignValue): self.__setattr('justify_content', value)

#     @property
#     def align_items(self) -> AlignValue:
#         '''Vertical alignment. 縱向排列，e.g. 靠上、居中、靠下'''
#         return self.__getattr('align_items') or CENTER
#     @align_items.setter
#     def align_items(self, value: AlignValue): self.__setattr('align_items', value)

#     @property
#     def z_index(self) -> int | None: return self.__getattr('z_index')
#     @z_index.setter
#     def z_index(self, value: int | None): self.__setattr('z_index', value)

#     @property
#     def font_size(self) -> int | None: return self.__getattr('font_size')
#     @font_size.setter
#     def font_size(self, value: int | None): self.__setattr('font_size', value)

#     @property
#     def font_name(self) -> str: return self.__getattr('font_name')
#     @font_name.setter
#     def font_name(self, value: str | None): self.__setattr('font_name', value)

#     @property
#     def color(self) -> ColorValue | None:
#         '''Font color.'''
#         return self.__getattr('color')
#     @color.setter
#     def color(self, value: ColorValue | None): self.__setattr('color', value)

#     def radius(self, el: ElementV2) -> float:
#         return (min(el.rect.width, el.rect.height) / 2) * self.radius_scale

# class ElementV2(pygame.sprite.Sprite, events.EventTarget):
#     __children: List[ElementV2]

#     scene: scenes.Scene | None = None
#     parent: ElementV2 | None = None
#     '''`.parent` is a READ ONLY property, please do not modify it.'''

#     __style = Style()

#     @property
#     def style(self):
#         return self.__style

#     @style.setter
#     def style(self, style: Style):
#         self.__style = style
#         def style_change_handler(event: events.StyleChangeEvent):
#             value = event.attr_value
#             match event.attr_name:
#                 case 'cursor':
#                     if value is None: self.remove_event_listener(events.CURSOR)
#                     else: self.add_event_listener(events.CURSOR)
#                 case 'cursor_r':
#                     if value is None: self.remove_event_listener(events.CURSOR_R)
#                     else: self.add_event_listener(events.CURSOR_R)
#                 case 'allow_flyout':
#                     if value: self.remove_event_listener(events._FLYOUT)
#                     else: self.add_event_listener(events._FLYOUT)
#                 case 'z_index':
#                     if self.scene: self.scene.reconnect_element(self)
#                 case _:
#                     if not self._create_with_surface:
#                         self.image = None
#         # 初始化
#         style.add_event_listener(events.STYLE_CHANGE, style_change_handler)
#         if style.cursor is None: self.remove_event_listener(events.CURSOR)
#         else: self.add_event_listener(events.CURSOR)
#         if style.cursor_r is None: self.remove_event_listener(events.CURSOR_R)
#         else: self.add_event_listener(events.CURSOR_R)
#         if style.allow_flyout: self.remove_event_listener(events._FLYOUT)
#         else: self.add_event_listener(events._FLYOUT)
#         if not self._create_with_surface:
#             self.image = None

#     @property # 在是一個過渡時期屬性，請在未來移除之
#     def cursor(self): return self.style.cursor
#     @cursor.setter
#     def cursor(self, value): self.style.cursor = value
#     @property # 在是一個過渡時期屬性，請在未來移除之
#     def cursor_r(self): return self.style.cursor_r
#     @cursor_r.setter
#     def cursor_r(self, value): self.style.cursor_r = value
#     @property # 在是一個過渡時期屬性，請在未來移除之
#     def allow_flyout(self): return self.style.allow_flyout
#     @allow_flyout.setter
#     def allow_flyout(self, value): self.style.allow_flyout = value
#     @property # 在是一個過渡時期屬性，請在未來移除之
#     def background_color(self): return self.style.background_color
#     @background_color.setter
#     def background_color(self, value): self.style.background_color = value

#     def apply(self, style: Style):
#         self.style = style
#         return self

#     @property
#     def children(self):
#         return tuple(self.__children)

#     def __init__(self, image: pygame.Surface | Style | None = None, children: Iterable[ElementV2] = []):
#         '''使用大小創建 Element 會將該大小設為此 Element 的 min_width 和 min_height'''
#         pygame.sprite.Sprite.__init__(self)
#         self.__attributes: Dict[str, Any] = dict()
#         if isinstance(image, Style):
#             self.apply(image)
#             self.image = None
#         else:
#             self.image = image
#         self.__children = list()
#         self.caches = CacheManager()
#         self.append_child(*children)

#     def get_attribute(self, name: str):
#         return self.__attributes.get(name)

#     def set_attribute(self, name: str, value: Any = None):
#         self.__attributes[name] = value

#     def remove_attribute(self, name: str):
#         del self.__attributes[name]
    
#     def has_attribute(self, name: str):
#         return name in self.__attributes

#     def point_in_radius(self, x: float, y: float):
#         return math.dist((x, y), self.rect.center) < self.radius

#     @property
#     def image(self) -> pygame.Surface:
#         return self.get_attribute('image')
    
#     @image.setter
#     def image(self, value: pygame.Surface | None):
#         style = self.style
#         if isinstance(value, pygame.Surface):
#             self._create_with_surface = True
#             rect = value.get_rect()
#         else:
#             self._create_with_surface = False
#             value = pygame.Surface((style.width or 0, style.height or 0))
#             rect = value.get_rect()
#             if style.x is not None:
#                 rect.x = style.x
#             if style.y is not None:
#                 rect.y = style.y
#         self.set_attribute('image', value)
#         self.rect = rect

#     @property
#     def radius(self) -> int:
#         return self.__style.radius(self)

#     def __len__(self):
#         return self.__children.__len__()

#     @property
#     def is_playing(self):
#         return False if self.scene is None else self.scene.is_playing

#     @property
#     def id(self) -> str | None: return self.get_attribute('id')
#     @id.setter
#     def id(self, value: str): self.set_attribute('id', value)

#     @property
#     def is_end_element(self):
#         '''是否為末端的元素'''
#         return self.style.display in (BLOCK, INLINE) and len(self) == 0

#     @property
#     def content_width(self) -> int:
#         cache = self.caches.get('content_w')
#         if cache is not None:
#             return cache
#         if self.is_end_element:
#             return_value = self.rect.width
#         else:
#             if self.style.display in (ROW, INLINE):
#                 return_value = sum(child.computed_width for child in self.__children) \
#                     + self.style.spacing * (len(self) - 1)
#             else:
#                 return_value = max(child.computed_width for child in self.__children)
#         return self.caches.set('content_w', return_value)

#     @property
#     def content_height(self) -> int:
#         cache = self.caches.get('content_h')
#         if cache is not None:
#             return cache
#         if self.is_end_element:
#             return_value = self.rect.height
#         else:
#             if self.style.display in (ROW, INLINE):
#                 return_value = max(child.computed_height for child in self.__children)
#             else:
#                 return_value = sum(child.computed_height for child in self.__children) \
#                     + self.style.spacing * (len(self) - 1)
#         return self.caches.set('content_h', return_value)

#     @property
#     def computed_width(self) -> int:
#         cache = self.caches.get('computed_w')
#         if cache is not None:
#             return cache
#         style = self.style
#         return_value = self.content_width + style.padding_left + style.padding_right if style.width is None else style.width
#         if style.min_width != None and return_value < style.min_width:
#             return_value = style.min_width
#         elif style.max_width != None and return_value > style.max_width:
#             return_value = style.max_width
#         return self.caches.set('computed_w', return_value)

#     @property
#     def computed_height(self) -> int:
#         cache = self.caches.get('computed_h')
#         if cache is not None:
#             return cache
#         style = self.style
#         return_value = self.content_height + style.padding_top + style.padding_bottom if style.height is None else style.height
#         if style.min_height != None and return_value < style.min_height:
#             return_value = style.min_height
#         elif style.max_height != None and return_value > style.max_height:
#             return_value = style.max_height
#         return self.caches.set('computed_h', return_value)

#     def compose(self):
#         '''Layouts (positions) itself and all child elements, but does not draw them. \\
#         排版不進行繪製。此方法也同時對所有層級的子元素作用。'''
#         self.rect.width = self.computed_width
#         self.rect.height = self.computed_height
#         style = self.style
#         if style.display in (ROW, INLINE):
#             # 設定 x 座標
#             if style.justify_content == START:
#                 x = self.rect.left + style.padding_left
#                 for child in self.__children:
#                     child.rect.left = x
#                     x += child.computed_width + style.spacing
#             elif style.justify_content == END:
#                 x = self.rect.right - style.padding_right
#                 for child in reversed(self.__children):
#                     child.rect.right = x
#                     x -= child.computed_width + style.spacing
#             else:
#                 x = self.rect.left + style.padding_left \
#                     + (self.computed_width - style.padding_left - style.padding_right) / 2 \
#                     - (self.content_width / 2)
#                 for child in self.__children:
#                     child.rect.left = x
#                     x += child.computed_width + style.spacing
#             # 設定 y 座標
#             if style.align_items == START:
#                 y = self.rect.top + style.padding_top
#                 for child in self.__children:
#                     child.rect.top = y
#             elif style.align_items == END:
#                 y = self.rect.bottom - style.padding_bottom
#                 for child in self.__children:
#                     child.rect.bottom = y
#             else:
#                 y = self.rect.centery
#                 for child in self.__children:
#                     child.rect.centery = y
#         else: # display in (COLUMN, BLOCK, default)
#             # 設定 x 座標
#             if style.justify_content == START:
#                 x = self.rect.left + style.padding_left
#                 for child in self.__children:
#                     child.rect.left = x
#             elif style.justify_content == END:
#                 x = self.rect.right - style.padding_right
#                 for child in self.__children:
#                     child.rect.right = x
#             else:
#                 x = self.rect.centerx
#                 for child in self.__children:
#                     child.rect.centerx = x
#             # 設定 y 座標
#             if style.align_items == START:
#                 y = self.rect.top + style.padding_top
#                 for child in self.__children:
#                     child.rect.top = y
#                     y += child.computed_height + style.spacing
#             elif style.align_items == END:
#                 y = self.rect.bottom - style.padding_bottom
#                 for child in reversed(self.__children):
#                     child.rect.bottom = y
#                     y -= child.computed_height + style.spacing
#             else:
#                 y = self.rect.top + style.padding_top \
#                     + (self.computed_height - style.padding_top - style.padding_bottom) / 2 \
#                     - (self.content_height / 2)
#                 for child in self.__children:
#                     child.rect.top = y
#                     y += child.computed_height + style.spacing
#         for child in self.__children:
#             child.compose()

#     @property
#     def parents(self) -> List[ElementV2]:
#         '''All parent elements of this element.'''
#         if self.parent is None:
#             return []
#         return self.parent.parents + [self.parent]

#     @property
#     def z_index(self) -> int:
#         z_index = self.style.z_index
#         if z_index is not None:
#             return z_index
#         if self.parent is None:
#             return 0
#         return self.parent.z_index + 1

#     def index(self, child: ElementV2):
#         '''Returns the index of the child'''
#         return self.__children.index(child)

#     def append_child(self, *children: ElementV2):
#         '''Appends elements to the end of the children of this element.'''
#         self.remove_child(*children)
#         self.__children.extend(children)
#         for child in children:
#             child.parent = self
#             child.connect_scene(self.scene)

#     def remove_child(self, *children: ElementV2):
#         '''Remove elements from children of this element.'''
#         for child in children:
#             if child in self.__children:
#                 self.__children.remove(child)
#                 child.parent = None
#                 child.disconnect_scene()

#     def insert_child(self, index: int, *children: ElementV2):
#         '''Insert elements into children of this element at the given index.'''
#         self.remove_child(*children)
#         for child in tuple(reversed(children)):
#             self.__children.insert(index, child)
#             child.parent = self
#             child.connect_scene(self.scene)
    
#     def move_child(self, new_parent: ElementV2, *children):
#         '''Move child elements from this element to another element.'''
#         self.remove_child(child for child in children)
#         new_parent.append_child(child for child in children)
    
#     def insert_before(self, node: ElementV2, *children: ElementV2):
#         '''Insert elements into children of this element before the given node(element).'''
#         if node not in self.__children:
#             raise 'node is not in children'
#         index = self.__children.index(node)
#         for child in tuple(reversed(children)):
#             self.insert_child(index, child)
    
#     def insert_after(self, node: ElementV2, *children: ElementV2):
#         '''Insert elements into children of this element after the given node(element).'''
#         if node not in self.__children:
#             raise 'node is not in children'
#         index = self.__children.index(node) + 1
#         for child in tuple(reversed(children)):
#             self.insert_child(index, child)

#     @property
#     def all_children(self) -> Tuple[ElementV2]:
#         '''All hierarchical child elements below this element.

#         在此元素之下所有層級的子元素。'''
#         watched = set()
#         parents = { self }
#         children = set()
#         while len(watched) != len(parents):
#             for parent in tuple(parents):
#                 if parent in watched:
#                     continue
#                 for child in parent.children:
#                     children.add(child)
#                     parents.add(child)
#                 watched.add(parent)
#         return tuple(children)

#     def connect_scene(self, scene: scenes.Scene | None):
#         '''Connect with the scene. (draw and update this element in the scene) \\
#         注：此方法僅在 scene 內和 self 內更動 children 時調用。此方法也同時對所有層級的子元素作用。'''
#         if scene is None: return
#         scene.connect_element(self)
#         self.scene = scene
#         for child in self.__children:
#             child.connect_scene(scene)

#     def disconnect_scene(self):
#         '''Disconnect with the scene. \\
#         注：此方法僅在 scene 內和 self 內更動 children 時調用。此方法也同時對所有層級的子元素作用。'''
#         if self.scene is None: return
#         self.scene.disconnect_element(self)
#         self.scene = None
#         for child in self.__children:
#             child.disconnect_scene()
    
#     def kill(self):
#         '''Remove the Element from all Groups. Remove all event listeners of the Element.'''
#         self.dispatch_event(events.KillEvent(self))
#         self.remove_all_event_listeners()
#         self.disconnect_scene()
#         pygame.sprite.Sprite.kill(self)

# class TextBoxV2(ElementV2):
#     def __init__(
#             self,
#             text: Any | refs.Ref,
#             font_size: int = 24,
#             font_color: ColorValue = FONT_COLOR,
#             font_background: ColorValue | None = None,
#             font_name: str = pygame.font.get_default_font(),
#             font_antialias: bool = True
#             ):
#         ElementV2.__init__(self)
#         self.ref = refs.to_ref(text)
#         self.font_antialias = font_antialias
#         self.update_font(font_name, font_size, font_color, font_background)
#         self.add_event_listener(events.REF_CHANGE, lambda: self.update_image())

#     def update_font(
#             self,
#             font_name: str | None = None,
#             font_size: int | None = None,
#             font_color: ColorValue = None,
#             font_background: ColorValue = None
#             ):
#         if font_name is not None:
#             self.__font_name = font_name
#         if font_size is not None:
#             self.__font_size = font_size
#         self.__font_color = font_color
#         self.__font_background = font_background
#         self.font = pygame.font.Font(self.font_name, self.font_size)
#         self.update_image()
#         return self.font

#     def update_image(self, text: str | None = None):
#         if text is not None:
#             self.ref.value = text
#         if self.font is None:
#             return
#         old_center = self.rect.center
#         self.image = self.font.render(self.text, self.font_antialias, self.font_color, self.font_background)
#         self.rect.center = old_center
#         return self.image

#     font: pygame.font.Font | None = None
#     __font_name: str = pygame.font.get_default_font()
#     __font_size: int = 12
#     __font_color: ColorValue | None = None
#     __font_background: ColorValue | None = None
#     __ref: refs.Ref[Any] | None = None

#     @property
#     def ref(self):
#         return self.__ref

#     @ref.setter
#     def ref(self, value: refs.Ref[Any]):
#         if self.__ref is not None:
#             self.__ref.unbind(self)
#         self.__ref = value
#         value.bind(self)
#         self.update_image()

#     @property
#     def text(self):
#         return str(self.ref.value)

#     @text.setter
#     def text(self, value: Any):
#         self.update_image(str(value))

#     @property
#     def font_name(self):
#         return self.__font_name

#     @font_name.setter
#     def font_name(self, value: str):
#         self.update_font(value)

#     @property
#     def font_size(self):
#         return self.__font_size

#     @font_size.setter
#     def font_size(self, value: int):
#         self.update_font(None, value)

#     @property
#     def font_color(self):
#         return self.__font_color or FONT_COLOR

#     @font_color.setter
#     def font_color(self, value: ColorValue):
#         self.update_font(None, None, value)

#     @property
#     def font_background(self):
#         return self.__font_background

#     @font_background.setter
#     def font_background(self, value: ColorValue):
#         self.update_font(None, None, None, value)
