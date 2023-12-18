import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes
from random import randint, sample

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    main_game.background_color = (0, 30, 0)

    schedule: list[levels.Spawner] = []

    # 0 - 30 seconds: 4zombie, 1bucket = 5
    for i in range(5):
        schedule.append(levels.ZombieSpawner(i * 5 * FPS, randint(0, 4), zombies.RegularZombie()))
    for i in sample(range(5), k=1):
        schedule.append(levels.ZombieSpawner(randint(30, 30) * FPS, i, zombies.BucketHeadZombie()))

    # 40 - 60 seconds: 2zombie, 2bucket, 1newpaper = 5
    for i in sample(range(5), k=2):
        schedule.append(levels.ZombieSpawner(randint(40, 60) * FPS, i, zombies.RegularZombie()))
    for i in sample(range(5), k=2):
        schedule.append(levels.ZombieSpawner(randint(40, 50) * FPS, i, zombies.BucketHeadZombie()))
    for i in sample(range(5), k=1):
        schedule.append(levels.ZombieSpawner(randint(50, 60) * FPS, i, zombies.NewspaperZombie()))

    # 60 - 120 seconds: 4zombie, 4bucket, 2newpaper = 10
    for i in sample(range(5), k=4):
        schedule.append(levels.ZombieSpawner(randint(70, 120) * FPS, i, zombies.RegularZombie()))
    for i in sample(range(5), k=4):
        schedule.append(levels.ZombieSpawner(randint(60, 100) * FPS, i, zombies.BucketHeadZombie()))
    for i in sample(range(5), k=2):
        schedule.append(levels.ZombieSpawner(randint(90, 120) * FPS, i, zombies.NewspaperZombie()))

    # 120 - 180 seconds: 10zombie, 6bucket, 4newpaper = 20
    for i in range(10):
        schedule.append(levels.ZombieSpawner(randint(140, 180) * FPS, randint(0, 4), zombies.RegularZombie()))
    for i in range(6):
        schedule.append(levels.ZombieSpawner(randint(120, 150) * FPS, randint(0, 4), zombies.BucketHeadZombie()))
    for i in range(4):
        schedule.append(levels.ZombieSpawner(randint(150, 180) * FPS, randint(0, 4), zombies.NewspaperZombie()))

    level = levels.Level(main_game, schedule)
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