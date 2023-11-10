import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

main_game = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    pass

main_game.init = init