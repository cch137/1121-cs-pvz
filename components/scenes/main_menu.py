import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes
import components.events as events

main_menu = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    main_menu.background_color = (0, 16, 0)
    
    title_el = Element(None, BLOCK, [
        TextBox('PLANTS VS ZOMBIES', 48, (48, 180, 48)),
        TextBox('植物大戰殭屍', 64, (160, 160, 160)),
    ])
    title_el.spacing = 8
    title_el.rect.center = (WINDOW_WIDTH/2, 250)
    main_menu.add_element(title_el)

    start_button = TextBox('開始遊戲', 48, (160, 20, 20))
    start_button.rect.center = (WINDOW_WIDTH/2, 600)
    def start_button_mouseenter(): start_button.font_color = (255, 32, 32)
    def start_button_mouseleave(): start_button.font_color = (160, 20, 20)
    start_button.add_event_listener(events.MOUSEENTER, start_button_mouseenter)
    start_button.add_event_listener(events.MOUSELEAVE, start_button_mouseleave)
    def onkeydown(e: events.KeydownEvent):
        if e.key == 32: controller.goto_scene(controller.scenes.main_game)
    start_button.add_event_listener(events.KEYDOWN, onkeydown)
    start_button.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.main_game))
    start_button.cursor = 'hand'
    main_menu.add_element(start_button)

    press_any_key_hint = TextBox('Press SPACE to start', 24, (128, 128, 128))
    press_any_key_hint.rect.centerx = WINDOW_WIDTH / 2
    press_any_key_hint.rect.bottom = WINDOW_HEIGHT / 2 + 160
    main_menu.add_element(press_any_key_hint)

main_menu.init = init

