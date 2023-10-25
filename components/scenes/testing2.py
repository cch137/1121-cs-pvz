from constants import *
import components.events as events
import components.scenes as scenes
import components.element as element
from components.controller import controller

testing2 = scenes.Scene()

def init():
    outer_element = element.Element()
    outer_element.min_width = WINDOW_WIDTH
    outer_element.min_height = WINDOW_HEIGHT

    inner_element = element.Element((600, 400))
    inner_element.min_width = 600
    inner_element.min_height = 400
    inner_element.background_color = (255, 0, 0)
    inner_element.spacing = 10

    btn1 = element.Element((300, 80))
    btn1.background_color = (0, 255, 0)
    btn2 = element.Element((300, 80))
    btn2.background_color = (0, 255, 0)
    btn3 = element.Element((300, 80), 'row')
    btn3.background_color = (0, 255, 0)
    btn3.spacing = 15

    btn3_1 = element.Element((75, 50))
    btn3_1.background_color = (0, 0, 255)
    btn3_2 = element.Element((75, 50))
    btn3_2.background_color = (0, 0, 255)
    btn3_3 = element.Element((75, 50))
    btn3_3.background_color = (0, 0, 255)

    outer_element.append_child(inner_element)
    inner_element.append_child(btn1, btn2, btn3)
    btn3.append_child(btn3_1, btn3_2, btn3_3)

    testing2.add_element(outer_element)

testing2.init = init
