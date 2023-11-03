import pygame
import utils.process as process
from constants import *
from components import controller

# 設置視窗圖標、標題，初始化視窗
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption(TITLE)
pygame.init()
pygame.mixer.init()

process.clear_caches()

def main():
    while controller.running:
        controller.play()
        process.update()

if __name__ == '__main__':
    controller.goto_scene(controller.scenes.main_menu)
    main()
