from components import *
from main import main

def make_color_block(color: (255, 255, 255)):
    ele = Element((100, 100))
    ele.x = 10
    ele.y = 10
    ele.background_color = color
    return ele

children = [make_color_block(c) for c in [
    (255, 0, 0), (0, 255, 0), (0, 0, 255)
]]

parent_ele = Element()
parent_ele.append_child(*children)

scene1 = Scene()

print(parent_ele.children)
print(children[0].children)
print(children[1].children)
print(children[2].children)

scene1.add_element(parent_ele)

print(scene1.elements)
print(scene1.layers)

main(scene1)