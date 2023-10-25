import pygame
from constants import *
from components import *

def make_color_block(color: (255, 255, 255)):
    ele = Element((50, 50))
    ele.background_color = color
    return ele

children = [make_color_block(c) for c in [
    (255, 0, 0), (0, 255, 0), (0, 0, 255)
]]

parent_ele = Element()

parent_ele.x = 50
parent_ele.y = 50

parent_ele.append_child(*children)

parent_ele.min_height = 200
parent_ele.min_width = 150
parent_ele.spacing = 25

def blue_clicked():
    print('blue clicked')

children[2].add_event_listener(events.CLICK, blue_clicked)

children[0].cursor = 'crosshair'
children[1].cursor = 'sizeall'
children[2].cursor = 'hand'

scene = Scene()

scene.add_element(parent_ele)

controller.goto_scene(scene)
