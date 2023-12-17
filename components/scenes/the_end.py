import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

the_end = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    level: levels.Level = controller.level

    bg_image = media.load_image('scenes/victory.png' if level.victory else 'scenes/game_over.png', WINDOW_SIZE)
    end_text = TextBox('你勝利了!' if level.victory else '你失敗了!', 56)
    end_text.rect.center = (528, 360)
    bg = Element(bg_image)
    the_end.add_element(bg)
    bg = Element(WINDOW_SIZE)
    bg.background_color = (8, 8, 8, 64)
    the_end.add_element(bg, end_text)

    ele = Element((315, 65))
    ele.background_color = (0,0,0,0)
    ele.cursor = 'hand'
    ele.rect.center = (528, 490)
    the_end.add_element(ele)
    def back_to_main_menu():
        controller.unload_sceen(controller.scenes.the_end)
        controller.goto_scene(controller.scenes.main_menu)
    ele.add_event_listener(events.CLICK, back_to_main_menu)

the_end.init = init


 