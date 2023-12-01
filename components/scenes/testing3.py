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
    back_btn.rect.topleft = (0, 0)
    testing3.add_element(back_btn)

    def use_zombie_move(zombie: zombies.Zombie, rate: float = -2):
        zombie.velocity_x = 0
        sleeping = 0
        velocity_sign = 0
        if rate < 0: velocity_sign = 1
        forward = True
        _update = zombie.update
        a = 0.6 * rate
        b = -0.1 * rate
        def zombie_move(*args, **kwargs):
            _update(*args, **kwargs)
            nonlocal sleeping
            nonlocal velocity_sign
            nonlocal forward
            if sleeping < 60:
                sleeping += 1
                return
            if rate >= 0:
                if velocity_sign == 0 and zombie.velocity_x < 0:
                    velocity_sign = 1
                elif velocity_sign == 1 and zombie.velocity_x >= 0:
                    velocity_sign = 0
                    sleeping = 0
                    zombie.velocity_x = 0
                    return
            else:
                if velocity_sign == 0 and zombie.velocity_x <= 0:
                    velocity_sign = 1
                    sleeping = 0
                    zombie.velocity_x = 0
                    return
                elif velocity_sign == 1 and zombie.velocity_x > 0:
                    velocity_sign = 0
            if forward:
                if (rate >= 0 and zombie.velocity_x < a) or (rate < 0 and zombie.velocity_x > a):
                    zombie.velocity_x += 0.0125 * rate
                else:
                    forward = False
            else:
                if (rate >= 0 and zombie.velocity_x > b) or (rate < 0 and zombie.velocity_x < b):
                    zombie.velocity_x -= 0.0125 * rate
                else:
                    forward = True
        zombie.update = zombie_move

    # 殭屍移動模擬
    zombie_demo = zombies.Zombie(pygame.Surface((20, 40)))
    zombie_demo.background_color = (0, 200, 100)
    zombie_demo.rect.center = (WINDOW_WIDTH, WINDOW_HEIGHT * 0.25)
    use_zombie_move(zombie_demo)
    testing3.add_element(zombie_demo)

testing3.init = init
