import pygame
from typing import *
from constants import *
import components.scenes as scenes

pause_menu = scenes.Scene()

def init():
    from components import Element, load_image, \
        events, Entity, Plant, Zombie, controller
    pass

pause_menu.init = init
