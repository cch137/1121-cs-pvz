from components import *
from main import main

scene1 = Scene()
ele1 = Element((100, 100))
ele1.x = 10
ele1.y = 10
ele1.background_color = (255, 0, 0)
scene1.add_element(ele1)

print(scene1.elements)

main(scene1)