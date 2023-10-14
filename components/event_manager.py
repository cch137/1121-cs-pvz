import pygame
import components.events as events
from components.element import Element

class EventManager():
    events = events
    __element_sets: dict[str, set[Element]] = {}

    def _elements_of(self, eventName: str):
        if eventName not in self.__element_sets:
            self.__element_sets[eventName] = set()
        return self.__element_sets[eventName]

    def addElement(self, element: Element, eventName: str):
        self._elements_of(eventName).add(element)

    def removeElement(self, element: Element, eventName: str):
        self._elements_of(eventName).remove(element)

    def init(self):
        pos = pygame.mouse.get_pos()
        x, y = pos

        # handle HoverEvent
        hover_event = events.HoverEvent(pos)
        for el in self._elements_of(events.HOVER):
            if el.rect.collidepoint(x, y):
                el.dispatchEvent(hover_event)

        # handle MouseEnterEvent and MouseLeaveEvent
        mouseenter_event = events.MouseEnterEvent(pos)
        mouseleave_event = events.MouseLeaveEvent(pos)
        l_mouseenter_spirits = self._elements_of(events.MOUSEENTER)
        l_mouseleave_spirits = self._elements_of(events.MOUSELEAVE)
        l_mouse_spirits = l_mouseenter_spirits | l_mouseleave_spirits # union
        for el in l_mouse_spirits:
            if el.rect.collidepoint(x, y):
                if not el.hasAttribute(events.HOVER):
                    el.setAttribute(events.HOVER, True)
                    if el in l_mouseenter_spirits:
                        el.dispatchEvent(mouseenter_event)
            elif el.hasAttribute(events.HOVER):
                if el.hasAttribute(events.HOVER):
                    el.removeAttribute(events.HOVER)
                    if el in l_mouseleave_spirits:
                        el.dispatchEvent(mouseleave_event)

    def handle(self, event: pygame.event.Event):
        # handle ClickEvent (左鍵)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            click_event = events.ClickEvent(event.pos, event.button)
            for el in self._elements_of(events.CLICK):
                if el.rect.collidepoint(x, y):
                    el.dispatchEvent(click_event)

event_manager = EventManager()
