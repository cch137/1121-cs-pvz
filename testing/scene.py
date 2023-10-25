from components import *
from main import main

def make_color_block(color: (255, 255, 255)):
    ele = Element((200, 50))
    ele.background_color = color
    return ele

children = [make_color_block(c) for c in [
    (255, 0, 0), (0, 255, 0), (0, 0, 255)
]]

parent_ele = Element()

print(parent_ele.x)
print(parent_ele.y)

parent_ele.x = 0
parent_ele.y = 0

parent_ele.append_child(*children)

parent_ele.min_height = 300
parent_ele.align_items = 'end'
print(parent_ele.computed_height)

scene1 = Scene()

scene1.add_element(parent_ele)

main(scene1)