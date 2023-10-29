import pygame
from typing import *
from constants import *
import components.scenes as scenes

pause_menu = scenes.Scene()

def init():
    from components import Element, load_image, load_animation, create_textbox, \
        events, Entity, Plant, Zombie, controller
    # helllo
    pass

pause_menu.init = init
