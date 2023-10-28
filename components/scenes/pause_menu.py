import pygame
from typing import *
from constants import *
import components.events as events
import components.scenes as scenes
import components.element as element
import components.entities as entities
import components.entities.plants as plants
import components.entities.zombies as zombies
from components.controller import controller

pause_menu = scenes.Scene()

def init():
    pass

pause_menu.init = init
