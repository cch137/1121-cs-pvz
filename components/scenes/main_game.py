import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
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
        pause_button_text = TextBox('PAUSE')
        pause_button = Element(None, None, [pause_button_text])
        pause_button.padding = 4
        pause_button_text.font_color = (255, 255, 255)
        pause_button.background_color = (0, 0, 0, 0)
        def _mouseenter():
            center = pause_button.rect.center
            pause_button_text.font_color = (240, 240, 240)
            pause_button.background_color = (0, 0, 0, 128)
            pause_button.image = pygame.Surface((pause_button.computed_width, pause_button.computed_height))
            pause_button.rect.center = center
        def _mouseleave():
            pause_button_text.font_color = (255, 255, 255)
            pause_button.background_color = (0, 0, 0, 0)
        pause_button.add_event_listener(events.MOUSEENTER, _mouseenter)
        pause_button.add_event_listener(events.MOUSELEAVE, _mouseleave)
        pause_button.add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.pause_menu))
        pause_button.compose()
        pause_button.rect.topright = (WINDOW_WIDTH - 8, 8)
        pause_button.cursor = 'hand'
        return pause_button
    
    main_game.add_element(PauseButton())

main_game.init = init