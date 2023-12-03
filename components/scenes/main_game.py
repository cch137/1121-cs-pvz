import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    level = levels.Level()
    controller.level = level
    main_game.add_element(level)
    
    bg = Element(media.load_image('scenes/game_map.jpg', (WINDOW_WIDTH, WINDOW_HEIGHT)))
    main_game.add_element(bg)

    def Tile(r: int, c: int):
        tile = Element((80,120))
        tile.id = f'tile-{r}-{c}'
        tile.background_color = (0, 0, 0, 0)
        def _mouseenter(): tile.background_color = (255, 255, 255, 55)
        def _mouseleave(): tile.background_color = (0, 0, 0, 0)
        tile.add_event_listener(events.MOUSEENTER, _mouseenter)
        tile.add_event_listener(events.MOUSELEAVE, _mouseleave)
        return tile
    
    game_map = Element(None, None, [Element(None, ROW, [Tile(r, c) for c in range(9)]) for r in range(5)])
    game_map.compose()
    game_map.rect.center = (475, 445)
    main_game.add_element(game_map)

    def PauseButton():
        button_text = TextBox('PAUSE')
        button = Element(None, None, [button_text])
        button.padding = 4
        button_text.font_color = (255, 255, 255)
        button.background_color = (0, 0, 0, 0)
        def _mouseenter():
            center = button.rect.center
            button_text.font_color = (240, 240, 240)
            button.background_color = (0, 0, 0, 128)
            button.image = pygame.Surface((button.computed_width, button.computed_height))
            button.rect.center = center
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

    def EndTestButton():
        button = TextBox('END TEST')
        button.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.the_end))
        button.rect.topleft = (8, 8)
        button.cursor = 'hand'
        return button
    
    main_game.add_element(EndTestButton())

main_game.init = init