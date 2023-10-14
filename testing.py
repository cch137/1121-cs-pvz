from components import *

x = Sprite((1,2))

def xOnClick1(e):
    print('x on click 1')

def xOnClick2():
    print('x on click 2')

x.addEventListener('click', xOnClick1)
x.addEventListener('click', xOnClick2)

x.dispatchEvent(event_manager.events.ClickEvent((0,0), 0))