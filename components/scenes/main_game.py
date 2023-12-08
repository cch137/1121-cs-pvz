import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    bg = Element(media.load_image('scenes/game_map.jpg', WINDOW_SIZE))
    main_game.add_element(bg)

    level = levels.Level(main_game, [
        levels.ZombieSpawner(1, 0, zombies.RegularZombie()),
        levels.ZombieSpawner(1, 1, zombies.RegularZombie()),
        levels.ZombieSpawner(1, 2, zombies.RegularZombie()),
        levels.ZombieSpawner(1, 3, zombies.RegularZombie()),
        levels.ZombieSpawner(1, 4, zombies.RegularZombie()),
        # levels.ZombieSpawner(1*FPS, 3, zombies.RegularZombie()),
        # levels.ZombieSpawner(2*FPS, 4, zombies.RegularZombie()),
        # levels.ZombieSpawner(3*FPS, 0, zombies.RegularZombie()),
        # levels.ZombieSpawner(4*FPS, 1, zombies.RegularZombie()),
    ])
    controller.level = level

    level.game_map.rect.center = (475, 445)
    level.card_board.rect.topleft = (level.game_map.rect.left, 8)

    def PauseButton():
        button_text = TextBox('PAUSE')
        button = Element(None, None, [button_text])
        button.padding = 4
        def _mouseenter():
            button_text.font_color = (240, 240, 240)
            button.background_color = (0, 0, 0, 128)
        def _mouseleave():
            button_text.font_color = (255, 255, 255)
            button.background_color = (0, 0, 0, 0)
        button.add_event_listener(events.MOUSEENTER, _mouseenter)
        button.add_event_listener(events.MOUSELEAVE, _mouseleave)
        button.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.pause_menu))
        button.compose()
        button.rect.topright = (WINDOW_WIDTH - 8, 8)
        button.cursor = 'hand'
        return button
    
    main_game.add_element(PauseButton())

    def TopLeftButtons():
        button1 = TextBox('END TEST')
        button1.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.the_end))
        button1.cursor = 'hand'
        button1.rect.topleft = (8, 8)
        return button1

    main_game.add_element(TopLeftButtons())

main_game.init = init