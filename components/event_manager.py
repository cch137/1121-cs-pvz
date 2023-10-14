import pygame
import components.events as events
from components.sprite import Sprite

class EventManager():
    events = events
    __sprites_sets: dict[str, set[Sprite]] = {}

    def _sprites_of(self, eventName: str):
        if eventName not in self.__sprites_sets:
            self.__sprites_sets[eventName] = set()
        return self.__sprites_sets[eventName]

    def addSprite(self, sprite: Sprite, eventName: str):
        self._sprites_of(eventName).add(sprite)

    def removeSprite(self, sprite: Sprite, eventName: str):
        self._sprites_of(eventName).remove(sprite)

    def init(self):
        pos = pygame.mouse.get_pos()
        x, y = pos

        # handle HoverEvent
        hover_event = events.HoverEvent(pos)
        for sprite in self._sprites_of(events.HOVER):
            if sprite.rect.collidepoint(x, y):
                sprite.dispatchEvent(hover_event)

        # handle MouseEnterEvent and MouseLeaveEvent
        mouseenter_event = events.MouseEnterEvent(pos)
        mouseleave_event = events.MouseLeaveEvent(pos)
        l_mouseenter_spirits = self._sprites_of(events.MOUSEENTER)
        l_mouseleave_spirits = self._sprites_of(events.MOUSELEAVE)
        l_mouse_spirits = l_mouseenter_spirits | l_mouseleave_spirits # union
        for sprite in l_mouse_spirits:
            if sprite.rect.collidepoint(x, y):
                if not sprite.hasAttribute(events.HOVER):
                    sprite.setAttribute(events.HOVER, True)
                    if sprite in l_mouseenter_spirits:
                        sprite.dispatchEvent(mouseenter_event)
            elif sprite.hasAttribute(events.HOVER):
                if sprite.hasAttribute(events.HOVER):
                    sprite.removeAttribute(events.HOVER)
                    if sprite in l_mouseleave_spirits:
                        sprite.dispatchEvent(mouseleave_event)

    def handle(self, event: pygame.event.Event):
        # handle ClickEvent (左鍵)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            click_event = events.ClickEvent(event.pos, event.button)
            for sprite in [s for s in self._sprites_of(events.CLICK) if s.rect.collidepoint(x, y)]:
                sprite.dispatchEvent(click_event)

event_manager = EventManager()
