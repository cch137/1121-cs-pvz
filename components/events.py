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
    def __init__(self) -> None:
        self.__listeners: Dict[str, Set[Callable]] = dict()
        self.__attributes: Dict[str, Any] = dict()

    def add_event_listener(self, eventName: str, listener: Callable | None = None):
        if eventName not in self.__listeners:
            self.__listeners[eventName] = set()
        self.__listeners[eventName].add(listener)
        event_manager.add_target(self, eventName)

    def remove_event_listener(self, eventName: str, listener: Callable | None = None):
        if eventName not in self.__listeners:
            return
        if listener in self.__listeners[eventName]:
            self.__listeners[eventName].remove(listener)
            if self.__listeners[eventName].__len__() == 0:
                event_manager.remove_target(self, eventName)
    
    def remove_all_event_listeners(self):
        for eventName in self.__listeners:
            listeners = set(self.__listeners[eventName])
            for listener in listeners:
                self.remove_event_listener(eventName, listener)

    def dispatch_event(self, event: UserEvent, callback: Callable | None = None):
        if event.name not in self.__listeners:
            return
        listeners = self.__listeners[event.name]
        if len(listeners) == 0:
            return
        tasks = set()
        for listener in listeners:
            try:
                args = (event, ) if listener.__code__.co_argcount > 0 else tuple()
                tasks.add(asynclib.wrapper(listener, *args))
            except Exception as err:
                print(err)
        async def _callback():
            await asyncio.gather(*tasks)
            if callback is not None:
                callback()
        asyncio.run(_callback())

    def get_attribute(self, name: str):
        return self.__attributes.get(name)

    def set_attribute(self, name: str, value: Any = None):
        self.__attributes[name] = value

    def remove_attribute(self, name: str):
        del self.__attributes[name]
    
    def has_attribute(self, name: str):
        return name in self.__attributes

class EventManager():
    __target_sets: Dict[str, Set[EventTarget]] = {}

    def _targets_of(self, eventName: str, writable: bool = False):
        if writable:
            return self.__target_sets.setdefault(eventName, set())
        else:
            return set(self.__target_sets.setdefault(eventName, set()))

    def _elements_of(self, *eventNames: str):
        return { el for els in tuple(self._targets_of(eventName) for eventName in eventNames) for el in els if isinstance(el, element.Element) and el.is_playing }

    def add_target(self, target: EventTarget, eventName: str):
        self._targets_of(eventName, True).add(target)

    def remove_target(self, target: EventTarget, eventName: str):
        self._targets_of(eventName, True).remove(target)

    def setup(self):
        from components import controller

        pos = pygame.mouse.get_pos()
        x, y = pos

        # dispatch HoverEvent
        for el in self._elements_of(HOVER, HOVER_R):
            if el.rect.collidepoint(x, y):
                el.dispatch_event(HoverEvent(pos, el))
            if el.point_in_radius(x, y):
                el.dispatch_event(HoverREvent(pos, el))

        # dispatch MouseEnterEvent and MouseLeaveEvent
        for el in self._elements_of(MOUSEENTER, MOUSELEAVE, MOUSEENTER_R, MOUSELEAVE_R):
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
        for el in self._elements_of(_FLYOUT):
            if el.rect.left > controller.screen_rect.right \
            or el.rect.right < controller.screen_rect.left \
            or el.rect.top > controller.screen_rect.bottom \
            or el.rect.bottom < controller.screen_rect.top:
                el.kill()

        # detect cursor style
        for el in reversed(sorted(self._elements_of(CURSOR), key=lambda x: x.z_index)):
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
        for el in reversed(sorted(self._elements_of(CURSOR_R), key=lambda x: x.z_index)):
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
        controller.cursor.default()

    def handle(self, event: pygame.event.Event):
        now = process.timestamp

        # dispatch ClickEvent
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for el in self._elements_of(CLICK, CLICK_R):
                if el.rect.collidepoint(x, y):
                    el.set_attribute(BUTTONDOWN, (event.button, now))
                if el.point_in_radius(x, y):
                    el.set_attribute(BUTTONDOWN_R, (event.button, now))
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            # mousedown 與 mouseup 之間的間隔在 1 秒內，且按下的按鍵相同，就會被判定為 click 事件
            for el in self._elements_of(CLICK):
                if el.has_attribute(BUTTONDOWN):
                    button, mousedown_at = el.get_attribute(BUTTONDOWN)
                    if el.rect.collidepoint(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(ClickEvent(event.pos, el))
                    el.remove_attribute(BUTTONDOWN)
            # click in radius 的判斷與 click 相同
            for el in self._elements_of(CLICK_R):
                if el.has_attribute(BUTTONDOWN_R):
                    button, mousedown_at = el.get_attribute(BUTTONDOWN_R)
                    if el.point_in_radius(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(ClickREvent(event.pos, el))
                    el.remove_attribute(BUTTONDOWN_R)

event_manager = EventManager()
