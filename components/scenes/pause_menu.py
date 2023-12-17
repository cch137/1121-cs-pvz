import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

pause_menu = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    pause_menu.background_color = (0, 30, 0)
    
    def Button(text: str, listener: Callable):
        def _():
            button = TextBox(text, 32)
            button.cursor = 'hand'
            def _mouseenter(): button.font_color = (128, 128, 128)
            def _mouseleave(): button.font_color = (255, 255, 255)
            button.add_event_listener(events.MOUSEENTER, _mouseenter)
            button.add_event_listener(events.MOUSELEAVE, _mouseleave)
            button.add_event_listener(events.CLICK, listener)
            return button
        return _()

    button_group = Element(None, None, [Button(t, l) for t, l in [
        ('繼續遊戲', lambda: controller.goto_scene(scenes.main_game)),
        ('重啟關卡', lambda: (scenes.main_game.reload(), controller.goto_scene(scenes.main_game))),
        ('返回主選單', lambda: controller.goto_scene(scenes.main_menu)),
    ]])
    button_group.background_color = (180 / 3.5, 134 / 3.5, 68 / 3.5)
    button_group.padding = (60, 80)
    button_group.spacing = 20
    pause_menu.add_element(button_group)
    button_group.compose()
    button_group.rect.center = controller.screen_rect.center

pause_menu.init = init
