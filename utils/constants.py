import typing
import pygame
import os

Coordinate = typing.Union[typing.Tuple[float, float], typing.Sequence[float], pygame.math.Vector2]
ColorValue = typing.Union[pygame.Color, int, str, typing.Tuple[int, int, int], typing.Tuple[int, int, int, int], typing.Sequence[int]]
DisplayValue = typing.Literal['block', 'inline', 'row', 'column']
AlignValue = typing.Literal['start','center','end']
CursorValue = typing.Union[None, int, typing.Literal['arrow','crosshair','hand','ibeam','sizeall','default']]

FPS = 60
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 760
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

TITLE = '植物大戰殭屍'

ASSETS_DIRNAME = os.path.abspath('assets/')

BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (250, 250, 250)

# Tiles background color:
# 1 2 1 2 1 2 ...
# 3 4 ...
# 1 2 ...
# 3 4 ...
# 1 2 ...
TILE_WIDTH = 80
TILE_HEIGHT = 120
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)
TILE_BG_1 = (1, 172, 31)
TILE_BG_2 = (0, 139, 20)
TILE_BG_3 = (28, 198, 36)
TILE_BG_4 = (20, 167, 26)

CARD_IMAGE_SIZE = (60, 60)
PLANT_SIZE = (60, 60)
BULLET_SIZE = (20, 20)
ZOMBIE_SIZE = (150, 150)
BULLET_SPEED = 15

MAP_COLUMNS = 9
MAP_ROWS = 5

# Spawner 生成多個殭屍時，殭屍之間的距離
ZOMBIES_GAP = 16

ROW = 'row'
COLUMN = 'column'
BLOCK = 'block'
INLINE = 'inline'
DISPLAY_MODES = (ROW, COLUMN, BLOCK, INLINE)

CENTER = 'center'
START = 'start'
END = 'end'

StyleAttrName = typing.Literal['display','x','y','width','height','min_width','max_width','min_height','max_height','background_color','radius_scale','cursor','cursor_r','allow_flyout','spacing','padding','padding_x','padding_y','padding_top','padding_bottom','padding_left','padding_right','justify_content','align_items','z_index','font_name','font_size','color']