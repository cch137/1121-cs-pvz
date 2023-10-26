from typing import *
import pygame
import utils.process as process

CURSOR = 'cursor'
CLICK = 'click'
HOVER = 'hover'
MOUSEENTER = 'mouseenter'
MOUSELEAVE = 'mouseleave'
BUTTONDOWN = 'buttondown'
BUTTONUP = 'buttonup'

class UserEvent():
    def __init__(self, name: str):
        self.name = name

class MouseEvent(UserEvent):
    def __init__(self, name: str, pos: tuple[int, int]):
        UserEvent.__init__(self, name)
        self.pos = pos

class HoverEvent(MouseEvent):
    def __init__(self, pos: tuple[int, int]):
        MouseEvent.__init__(self, HOVER, pos)

class MouseEnterEvent(MouseEvent):
    def __init__(self, pos: tuple[int, int]):
        MouseEvent.__init__(self, MOUSEENTER, pos)

class MouseLeaveEvent(MouseEvent):
    def __init__(self, pos: tuple[int, int]):
        MouseEvent.__init__(self, MOUSELEAVE, pos)

class ClickEvent(UserEvent):
    def __init__(self, pos: tuple[int, int]):
        MouseEvent.__init__(self, CLICK, pos)

class EventTarget():
    __listeners: dict[str, set[Callable]]
    __attributes: dict[str, Any]

    def __init__(self) -> None:
        self.__listeners = dict()
        self.__attributes = dict()

    def add_event_listener(self, eventName: str, listener: Callable | None = None):
        if eventName not in self.__listeners:
            self.__listeners[eventName] = set()
        if listener is not None:
            self.__listeners[eventName].add(listener)
        event_manager.add_target(self, eventName)

    def remove_event_listener(self, eventName: str, listener: Callable | None = None):
        if eventName not in self.__listeners:
            return
        if listener not in self.__listeners[eventName]:
            return
        if listener is not None:
            self.__listeners[eventName].remove(listener)
        if self.__listeners[eventName].__len__() == 0:
            event_manager.remove_target(self, eventName)

    def dispatch_event(self, event: UserEvent):
        if event.name in self.__listeners:
            for listener in self.__listeners[event.name]:
                try:
                    if listener.__code__.co_argcount > 0: listener(event)
                    else: listener()
                except Exception as err:
                    print(err)

    def get_attribute(self, name: str):
        return self.__attributes.get(name)

    def set_attribute(self, name: str, value):
        self.__attributes[name] = value

    def remove_attribute(self, name: str):
        del self.__attributes[name]
    
    def has_attribute(self, name: str):
        return name in self.__attributes

class EventManager():
    __target_sets: dict[str, set[EventTarget]] = {}

    def _targets_of(self, eventName: str, writable: bool = False):
        if eventName not in self.__target_sets:
            self.__target_sets[eventName] = set()
        if writable:
            return self.__target_sets[eventName]
        else:
            return self.__target_sets[eventName].copy()

    def add_target(self, target: EventTarget, eventName: str):
        self._targets_of(eventName, True).add(target)

    def remove_target(self, target: EventTarget, eventName: str):
        self._targets_of(eventName, True).remove(target)

    def init(self):
        import components.element
        from components.controller import controller

        pos = pygame.mouse.get_pos()
        x, y = pos

        # dispatch HoverEvent
        hover_event = HoverEvent(pos)
        for el in self._targets_of(HOVER):
            if el.rect.collidepoint(x, y):
                el.dispatch_event(hover_event)

        # dispatch MouseEnterEvent and MouseLeaveEvent
        mouseenter_event = MouseEnterEvent(pos)
        mouseleave_event = MouseLeaveEvent(pos)
        l_mouseenter = self._targets_of(MOUSEENTER)
        l_mouseleave = self._targets_of(MOUSELEAVE)
        l_mouse = l_mouseenter | l_mouseleave # union
        for el in l_mouse:
            if el.rect.collidepoint(x, y):
                if not el.has_attribute(HOVER):
                    el.set_attribute(HOVER, True)
                    if el in l_mouseenter:
                        el.dispatch_event(mouseenter_event)
            elif el.has_attribute(HOVER):
                if el.has_attribute(HOVER):
                    el.remove_attribute(HOVER)
                    if el in l_mouseleave:
                        el.dispatch_event(mouseleave_event)
        
        # detect cursor style
        l_cursor = { el for el in self._targets_of(CURSOR) if type(el) is components.element.Element }
        for el in reversed(sorted(l_cursor, key=lambda x: x.z_index)):
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
                    if type(el.cursor) is int:
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
            for el in self._targets_of(CLICK):
                if el.rect.collidepoint(x, y):
                    el.set_attribute(BUTTONDOWN, (event.button, now))
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            click_event = ClickEvent(event.pos)
            for el in self._targets_of(CLICK):
                if el.has_attribute(BUTTONDOWN):
                    # mousedown 與 mouseup 之間的間隔在 1 秒內，且按下的按鍵相同，就會被判定為 click 事件
                    button, mousedown_at = el.get_attribute(BUTTONDOWN)
                    if el.rect.collidepoint(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(click_event)
                    el.remove_attribute(BUTTONDOWN)

event_manager = EventManager()
