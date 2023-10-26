import pygame
from typing import *
from constants import *
import components.events as events
import components.scenes as scenes
import components.element as element
from components.controller import controller

testing1 = scenes.Scene()

def init():
    def make_color_block(color: (255, 255, 255)):
        ele = element.Element((50, 50))
        ele.background_color = color
        return ele

    children = [make_color_block(c) for c in [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
    ]]

    parent_ele = element.Element()
    parent_ele.min_width = 150
    parent_ele.max_height = 400
    parent_ele.x = 50
    parent_ele.y = 50
    parent_ele.spacing = 25
    parent_ele.append_child(*children)

    def blue_clicked():
        print('blue clicked')

    children[0].cursor = 'crosshair'
    children[1].cursor = 'sizeall'
    children[2].cursor = 'ibeam'
    children[3].cursor = 'hand'

    children[2].add_event_listener(events.CLICK, blue_clicked)

    # image element
    image_ele = element.Element(element.load_image('icon.png', (50, 50)))
    image_ele.cursor = 'hand'
    def image_ele_clicked():
        image_ele.image = pygame.transform.flip(image_ele.image, True, False)
    image_ele.add_event_listener(events.CLICK, image_ele_clicked)
    parent_ele.append_child(image_ele)

    parent_ele.append_child(children[3])
    def goto_testing2():
        controller.goto_scene(controller.scenes.testing2)
    children[3].add_event_listener(events.CLICK, goto_testing2)

    testing1.add_element(parent_ele)

testing1.init = init
