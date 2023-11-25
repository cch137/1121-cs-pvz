from typing import Callable, Any, Set, Dict
from utils.constants import Coordinate
import pygame
import asyncio
import utils.process as process
import utils.asynclib as asynclib
import components.element as element

CURSOR = 'cursor'
CLICK = 'click'
HOVER = 'hover'
MOUSEENTER = 'mouseenter'
MOUSELEAVE = 'mouseleave'
BUTTONDOWN = 'buttondown'
BUTTONUP = 'buttonup'

CURSOR_R = 'cursor_r'
CLICK_R = 'click_r'
HOVER_R = 'hover_r'
MOUSEENTER_R = 'mouseenter_r'
MOUSELEAVE_R = 'mouseleave_r'
BUTTONDOWN_R = 'buttondown_r'
BUTTONUP_R = 'buttonup_r'

REF_CHANGE = 'ref_change'
CHANGE = 'change'
STYLE_CHANGE = 'style_change'

_FLYOUT = 'flyout'
KILL = 'KILL'

# Custom Events
SUN_CHANGES = 'suns_change'

class EventTarget: pass

class UserEvent():
    def __init__(self, name: str, target: EventTarget | None = None):
        self.name = name
        self.target = target

class MouseEvent(UserEvent):
    def __init__(self, name: str, pos: Coordinate, target: EventTarget | None = None):
        UserEvent.__init__(self, name, target)
        self.pos = pos

class HoverEvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, HOVER, pos, target)

class MouseEnterEvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, MOUSEENTER, pos, target)

class MouseLeaveEvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, MOUSELEAVE, pos, target)

class ClickEvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, CLICK, pos, target)

class HoverREvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, HOVER_R, pos, target)

class MouseEnterREvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, MOUSEENTER_R, pos, target)

class MouseLeaveREvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, MOUSELEAVE_R, pos, target)

class ClickREvent(MouseEvent):
    def __init__(self, pos: Coordinate, target: EventTarget | None = None):
        MouseEvent.__init__(self, CLICK_R, pos, target)

class RefChangeEvent(UserEvent):
    def __init__(self, target: EventTarget | None = None):
        UserEvent.__init__(self, REF_CHANGE, target)

class StyleChangeEvent(UserEvent):
    def __init__(self, target: EventTarget | None = None, attr_name: str | None = None, attr_value: Any = None):
        self.attr_name = attr_name
        self.attr_value = attr_value
        UserEvent.__init__(self, REF_CHANGE, target)

class ChangeEvent(UserEvent):
    def __init__(self, target: EventTarget | None = None):
        UserEvent.__init__(self, CHANGE, target)

class KillEvent(UserEvent):
    def __init__(self, target: EventTarget | None = None):
        UserEvent.__init__(self, KILL, target)

class SunsChangeEvent(UserEvent):
    def __init__(self, target: EventTarget | None = None):
        UserEvent.__init__(self, SUN_CHANGES, target)

class EventTarget():
    __listeners: Dict[str, Set[Callable]] | None = None

    def add_event_listener(self, eventName: str, listener: Callable | None = None):
        if not self.__listeners:
            self.__listeners = dict()
        if eventName not in self.__listeners:
            self.__listeners[eventName] = set()
        self.__listeners[eventName].add(listener)
        if isinstance(self, element.Element):
            el_event_handler.add_target(self, eventName)

    def remove_event_listener(self, eventName: str, listener: Callable | None = None):
        if not self.__listeners:
            return
        if eventName not in self.__listeners:
            return
        if listener in self.__listeners[eventName]:
            self.__listeners[eventName].remove(listener)
            if self.__listeners[eventName].__len__() == 0:
                if isinstance(self, element.Element):
                    el_event_handler.remove_target(self, eventName)

    def remove_all_event_listeners(self):
        if not self.__listeners:
            return
        for eventName, listeners in self.__listeners.items():
            for listener in tuple(listeners):
                self.remove_event_listener(eventName, listener)

    def dispatch_event(self, event: UserEvent, callback: Callable | None = None, _async=True):
        if not self.__listeners:
            return
        if event.name not in self.__listeners:
            return
        listener_zip = tuple((l, (event, ) if l.__code__.co_argcount > 0 else tuple()) for l in self.__listeners[event.name])
        if len(listener_zip) == 0:
            return
        if _async:
            tasks = set()
            for listener, args in listener_zip:
                try:
                    tasks.add(asynclib.wrapper(listener, *args))
                except Exception as err:
                    print(err)
            async def _callback():
                await asyncio.gather(*tasks)
                if callback is not None:
                    callback()
            try:
                asyncio.run(_callback())
            except Exception as err:
                asynclib.run_threads(lambda: asyncio.run(_callback()))
        else:
            for listener, args in listener_zip:
                try:
                    listener(*args)
                except Exception as err:
                    print(err)

class ElementEventHandler():
    __target_sets: Dict[str, Set[element.Element]] = {}

    def __targets_of(self, eventName: str, writable: bool = False):
        if writable:
            return self.__target_sets.setdefault(eventName, set())
        else:
            return set(self.__target_sets.setdefault(eventName, set()))

    def targets_of(self, *eventNames: str):
        return { el for els in tuple(self.__targets_of(eventName) for eventName in eventNames) for el in els if el.is_playing }

    def add_target(self, target: element.Element, eventName: str):
        self.__targets_of(eventName, True).add(target)

    def remove_target(self, target: element.Element, eventName: str):
        self.__targets_of(eventName, True).remove(target)

    def setup(self):
        from components import controller

        pos = pygame.mouse.get_pos()
        x, y = pos

        # dispatch HoverEvent
        for el in self.targets_of(HOVER, HOVER_R):
            if el.rect.collidepoint(x, y):
                el.dispatch_event(HoverEvent(pos, el))
            if el.point_in_radius(x, y):
                el.dispatch_event(HoverREvent(pos, el))

        # dispatch MouseEnterEvent and MouseLeaveEvent
        for el in self.targets_of(MOUSEENTER, MOUSELEAVE, MOUSEENTER_R, MOUSELEAVE_R):
            if el.rect.collidepoint(x, y):
                if not el.has_attribute(HOVER):
                    el.dispatch_event(MouseEnterEvent(pos, el))
                    el.set_attribute(HOVER, True)
            elif el.has_attribute(HOVER):
                el.remove_attribute(HOVER)
                el.dispatch_event(MouseLeaveEvent(pos, el))
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
        for el in self.targets_of(_FLYOUT):
            rect = el.rect
            if rect.left > screen_right or rect.right < screen_left\
            or rect.top > screen_bottom or rect.bottom < screen_top:
                el.kill()

        # detect cursor style
        for el in reversed(sorted(self.targets_of(CURSOR_R), key=lambda x: x.z_index)):
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
        for el in reversed(sorted(self.targets_of(CURSOR), key=lambda x: x.z_index)):
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for el in self.targets_of(CLICK, CLICK_R):
                if el.rect.collidepoint(x, y):
                    el.set_attribute(BUTTONDOWN, (event.button, now))
                if el.point_in_radius(x, y):
                    el.set_attribute(BUTTONDOWN_R, (event.button, now))
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            # mousedown 與 mouseup 之間的間隔在 1 秒內，且按下的按鍵相同，就會被判定為 click 事件
            for el in self.targets_of(CLICK):
                if el.has_attribute(BUTTONDOWN):
                    button, mousedown_at = el.get_attribute(BUTTONDOWN)
                    if el.rect.collidepoint(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(ClickEvent(event.pos, el))
                    el.remove_attribute(BUTTONDOWN)
            # click in radius 的判斷與 click 相同
            for el in self.targets_of(CLICK_R):
                if el.has_attribute(BUTTONDOWN_R):
                    button, mousedown_at = el.get_attribute(BUTTONDOWN_R)
                    if el.point_in_radius(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(ClickREvent(event.pos, el))
                    el.remove_attribute(BUTTONDOWN_R)

el_event_handler = ElementEventHandler()
