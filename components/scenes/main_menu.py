import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes
import components.events as events

main_menu = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    title_el = TextBox('PLANTS VS ZOMBIES', 36, TILE_BG_3)
    title_el.rect.center = (WINDOW_WIDTH/2, 250)
    main_menu.add_element(title_el)

    start_button = TextBox('CLICK TO START')
    start_button.rect.center = (WINDOW_WIDTH/2, 600)
    start_button.add_event_listener(events.KEYDOWN, lambda: controller.goto_scene(controller.scenes.main_game))
    start_button.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.main_game))
    start_button.cursor = 'hand'
    main_menu.add_element(start_button)

    press_any_key_hint = TextBox('press any key to start', 18, (128, 128, 128))
    press_any_key_hint.rect.centerx = WINDOW_WIDTH / 2
    press_any_key_hint.rect.bottom = WINDOW_HEIGHT / 2 + 160
    main_menu.add_element(press_any_key_hint)

main_menu.init = init

