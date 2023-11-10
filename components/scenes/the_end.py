import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

the_end = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, Plant, Zombie, controller, levels
    pass

the_end.init = init
