import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

testing3 = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    back_btn = TextBox('Back')
    back_btn.cursor = 'hand'
    back_btn.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.testing2))
    def _back_btn_mouseenter(): back_btn.font_color = (0, 0, 255)
    def _back_btn_mouseleave(): back_btn.font_color = (255, 255, 255)
    back_btn.add_event_listener(events.MOUSEENTER, _back_btn_mouseenter)
    back_btn.add_event_listener(events.MOUSELEAVE, _back_btn_mouseleave)
    back_btn.rect.topleft = (0, 0)
    testing3.add_element(back_btn)

    # 殭屍移動模擬
    zombie_demo = zombies.Zombie(pygame.Surface((20, 40)))
    zombie_demo.background_color = (0, 200, 100)
    zombie_demo.rect.center = (WINDOW_WIDTH, WINDOW_HEIGHT * 0.25)
    zombie_demo.update = zombies.zombie_mover(zombie_demo)
    testing3.add_element(zombie_demo)

testing3.init = init
