import pygame
from constants import *
import utils.process as process
from components import controller, event_manager, Scene

# 設置視窗圖標、標題，初始化視窗
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption(TITLE)
pygame.init()

process.clear_caches()

def main():
    while controller.running:
        controller.play()
        process.update()

if __name__ == '__main__':
    main()
