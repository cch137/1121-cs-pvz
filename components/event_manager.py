import time
import pygame
import components.events as events
from components.element import EventTarget

class EventManager():
    events = events
    __element_sets: dict[str, set[EventTarget]] = {}

    def _elements_of(self, eventName: str):
        if eventName not in self.__element_sets:
            self.__element_sets[eventName] = set()
        return self.__element_sets[eventName]

    def add_element(self, element: EventTarget, eventName: str):
        self._elements_of(eventName).add(element)

    def remove_element(self, element: EventTarget, eventName: str):
        self._elements_of(eventName).remove(element)

    def init(self):
        pos = pygame.mouse.get_pos()
        x, y = pos

        # dispatch HoverEvent
        hover_event = events.HoverEvent(pos)
        for el in self._elements_of(events.HOVER):
            if el.rect.collidepoint(x, y):
                el.dispatch_event(hover_event)

        # dispatch MouseEnterEvent and MouseLeaveEvent
        mouseenter_event = events.MouseEnterEvent(pos)
        mouseleave_event = events.MouseLeaveEvent(pos)
        l_mouseenter_spirits = self._elements_of(events.MOUSEENTER)
        l_mouseleave_spirits = self._elements_of(events.MOUSELEAVE)
        l_mouse_spirits = l_mouseenter_spirits | l_mouseleave_spirits # union
        for el in l_mouse_spirits:
            if el.rect.collidepoint(x, y):
                if not el.has_attribute(events.HOVER):
                    el.set_attribute(events.HOVER, True)
                    if el in l_mouseenter_spirits:
                        el.dispatch_event(mouseenter_event)
            elif el.has_attribute(events.HOVER):
                if el.has_attribute(events.HOVER):
                    el.remove_attribute(events.HOVER)
                    if el in l_mouseleave_spirits:
                        el.dispatch_event(mouseleave_event)

    def handle(self, event: pygame.event.Event):
        now = time.time()

        # dispatch ClickEvent
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for el in self._elements_of(events.CLICK):
                if el.rect.collidepoint(x, y):
                    el.set_attribute(events.BUTTONDOWN, (event.button, now))
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            click_event = events.ClickEvent(event.pos)
            for el in self._elements_of(events.CLICK):
                if el.has_attribute(events.BUTTONDOWN):
                    # mousedown 與 mouseup 之間的間隔在 1 秒內，且按下的按鍵相同，就會被判定為 click 事件
                    button, mousedown_at = el.get_attribute(events.BUTTONDOWN)
                    if el.rect.collidepoint(x, y) \
                        and button == event.button \
                        and now - mousedown_at < 1:
                        if event.button == pygame.BUTTON_LEFT:
                            el.dispatch_event(click_event)
                    el.remove_attribute(events.BUTTONDOWN)

event_manager = EventManager()
