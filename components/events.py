from typing import Callable, Any, Set, Dict
from utils.constants import Coordinate
import asyncio
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

KEYDOWN = 'keydown'

REF_CHANGE = 'ref_change'
CHANGE = 'change'
STYLE_CHANGE = 'style_change'

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

class KeydownEvent(MouseEvent):
    def __init__(self, key: Any, target: EventTarget | None = None):
        UserEvent.__init__(self, KEYDOWN, target)

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
            element.event_handler.add_target(self, eventName)

    def remove_event_listener(self, eventName: str, listener: Callable | None = None):
        if not self.__listeners:
            return
        if eventName not in self.__listeners:
            return
        if listener in self.__listeners[eventName]:
            self.__listeners[eventName].remove(listener)
            if self.__listeners[eventName].__len__() == 0:
                if isinstance(self, element.Element):
                    element.event_handler.remove_target(self, eventName)

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
