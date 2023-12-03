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
    
    game_map = Element()

    for r in range(5):
        row = Element()
        row.display = ROW
        for c in range(9):
            tile = Element((80,120))
            tile.id = f'tile-{r}-{c}'
            tile.background_color = (0, 0, 0, 0)
            row.append_child(tile)
        game_map.append_child(row)
    game_map.compose()
    game_map.rect.center = (475, 445)

    main_game.add_element(game_map)
    
         
    
       
       

main_game.init = init