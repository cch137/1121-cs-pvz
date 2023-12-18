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
TILE_WIDTH = 90
TILE_HEIGHT = 110
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)
BRIGHTNESS = 0.6
TILE_BG_1 = (1 * BRIGHTNESS, 172 * BRIGHTNESS, 31 * BRIGHTNESS, 200)
TILE_BG_2 = (0 * BRIGHTNESS, 139 * BRIGHTNESS, 20 * BRIGHTNESS, 200)
TILE_BG_3 = (28 * BRIGHTNESS, 198 * BRIGHTNESS, 36 * BRIGHTNESS, 200)
TILE_BG_4 = (20 * BRIGHTNESS, 167 * BRIGHTNESS, 26 * BRIGHTNESS, 200)

CARD_IMAGE_SIZE = (75, 75)
PLANT_SIZE = (96, 96)
BULLET_SIZE = (18, 18)
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