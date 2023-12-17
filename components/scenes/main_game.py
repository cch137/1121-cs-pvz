import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    main_game.background_color = (0, 30, 0)

    level = levels.Level(main_game, [
        levels.ZombieSpawner(0, 0, zombies.NewspaperZombie()),
        levels.ZombieSpawner(0, 1, zombies.NewspaperZombie()),
        levels.ZombieSpawner(0, 2, zombies.NewspaperZombie()),
        levels.ZombieSpawner(0, 3, zombies.NewspaperZombie()),
        levels.ZombieSpawner(0, 4, zombies.NewspaperZombie()),
        # levels.ZombieSpawner(1, 2, zombies.RegularZombie()),
        # levels.ZombieSpawner(1, 3, zombies.RegularZombie()),
        # levels.ZombieSpawner(1, 4, zombies.RegularZombie()),
        # levels.ZombieSpawner(1*FPS, 3, zombies.RegularZombie()),
        # levels.ZombieSpawner(2*FPS, 4, zombies.RegularZombie()),
        # levels.ZombieSpawner(3*FPS, 0, zombies.RegularZombie()),
        # levels.ZombieSpawner(4*FPS, 1, zombies.RegularZombie()),
    ])
    controller.level = level

    level.game_map.rect.center = (471, 462)
    level.card_board.rect.topleft = (level.game_map.rect.left, 18)

    def PauseButton():
        button_text = TextBox('PAUSE')
        button = Element(None, None, [button_text])
        button.padding = 4
        def _mouseenter():
            button_text.font_color = (240, 240, 240)
            button.background_color = (255, 0, 0, 128)
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

main_game.init = init