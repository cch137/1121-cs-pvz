from constants import *
from components import *
from main import main

outer_element = Element()
outer_element.min_width = WINDOW_WIDTH
outer_element.min_height = WINDOW_HEIGHT

inner_element = Element((600, 400))
inner_element.min_width = 600
inner_element.min_height = 400
inner_element.background_color = (255, 0, 0)
inner_element.spacing = 10

btn1 = Element((300, 80))
btn1.background_color = (0, 255, 0)
btn2 = Element((300, 80))
btn2.background_color = (0, 255, 0)
btn3 = Element((300, 80))
btn3.background_color = (0, 255, 0)

outer_element.append_child(inner_element)
inner_element.append_child(btn1, btn2, btn3)

scene = Scene()

scene.add_element(outer_element)

scene.compose()

main(scene)