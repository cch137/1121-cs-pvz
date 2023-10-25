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
btn3 = Element((300, 80), 'row')
btn3.background_color = (0, 255, 0)
btn3.spacing = 15

btn3_1 = Element((75, 50))
btn3_1.background_color = (0, 0, 255)
btn3_2 = Element((75, 50))
btn3_2.background_color = (0, 0, 255)
btn3_3 = Element((75, 50))
btn3_3.background_color = (0, 0, 255)

outer_element.append_child(inner_element)
inner_element.append_child(btn1, btn2, btn3)
btn3.append_child(btn3_1, btn3_2, btn3_3)

print(btn3.children)

scene = Scene()

scene.add_element(outer_element)

scene.compose()

main(scene)