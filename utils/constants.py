import typing
import pygame
import os

Coordinate = typing.Union[typing.Tuple[float, float], typing.Sequence[float], pygame.math.Vector2]
ColorValue = typing.Union[pygame.Color, int, str, typing.Tuple[int, int, int], typing.Tuple[int, int, int, int], typing.Sequence[int]]

FPS = 60
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 760

TITLE = '植物大戰殭屍'

ASSETS_DIRNAME = os.path.abspath('assets/')

BACKGROUND_COLOR = (20, 22, 24)
FONT_COLOR = (250, 250, 250)

# Tiles background color:
# 1 2 1 2 1 2 ...
# 3 4 ...
# 1 2 ...
# 3 4 ...
# 1 2 ...
TILE_WIDTH = 100
TILE_HEIGHT = 120
TILE_BG_1 = (1, 172, 31)
TILE_BG_2 = (0, 139, 20)
TILE_BG_3 = (28, 198, 36)
TILE_BG_4 = (20, 167, 26)

MAP_COLUMNS = 9
MAP_ROWS = 5

ROW = 'row'
COLUMN = 'column'
BLOCK = 'block'
INLINE = 'inline'
DISPLAY_MODES = (ROW, COLUMN, BLOCK, INLINE)

CENTER = 'center'
START = 'start'
END = 'end'
