import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes
from random import randint

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    main_game.background_color = (0, 30, 0)

    gap = 15 * FPS

    level = levels.Level(main_game, [
        levels.ZombieSpawner(0 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(1 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(2 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(3 * gap, randint(0, 1), zombies.RegularZombie()),
        levels.ZombieSpawner(3 * gap, randint(3, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(3 * gap, randint(2, 2), zombies.BucketHeadZombie()),
        levels.ZombieSpawner(4 * gap, randint(1, 4), zombies.BucketHeadZombie(), zombies.RegularZombie(), zombies.RegularZombie()),
        levels.ZombieSpawner(4 * gap, randint(4, 4), zombies.NewspaperZombie()),
        levels.ZombieSpawner(5 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(5 * gap, randint(0, 4), zombies.BucketHeadZombie()),
        levels.ZombieSpawner(5 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(6 * gap, randint(0, 4), zombies.BucketHeadZombie()),
        levels.ZombieSpawner(6 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(7 * gap, randint(0, 0), zombies.NewspaperZombie()),
        levels.ZombieSpawner(8 * gap, randint(1, 1), zombies.BucketHeadZombie(), zombies.BucketHeadZombie()),
        levels.ZombieSpawner(9 * gap, randint(2, 2), zombies.NewspaperZombie()),
        levels.ZombieSpawner(10 * gap, randint(3, 3), zombies.BucketHeadZombie(), zombies.BucketHeadZombie()),
        levels.ZombieSpawner(10 * gap, randint(4, 4), zombies.NewspaperZombie()),
        levels.ZombieSpawner(10.25 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(10.5 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(10.75 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(11 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(11.5 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(12 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(12.25 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(12.5 * gap, randint(0, 4), zombies.RegularZombie()),
        levels.ZombieSpawner(12.75 * gap, randint(0, 4), zombies.RegularZombie()),
    ])
    controller.level = level

    level.game_map.rect.center = (471, 462)
    level.card_board.rect.topleft = (level.game_map.rect.left, 18)

    def PauseButton():
        button_text = TextBox('暫停遊戲')
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