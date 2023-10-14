from components import *

x = Sprite((1,2))

def xOnClick():
    print('x on click')

x.addEventListener('click', xOnClick)

x.dispatchEvent('click')