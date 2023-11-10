import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

pause_menu = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    pass

pause_menu.init = init
