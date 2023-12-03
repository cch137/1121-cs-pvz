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

main_game.init = init