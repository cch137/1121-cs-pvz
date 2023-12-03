import time
t0 = time.time()
import pygame
import utils.process as process
from utils.constants import *
from components import controller, media

# 設置視窗圖標、標題，初始化視窗
pygame.display.set_icon(media.load_image('icon.png'))
pygame.display.set_caption(TITLE)
pygame.mixer.pre_init(44100, 16, 2, 4096)  # 性能優化
pygame.mixer.init()
pygame.init()
process.clear_caches()

def main():
    while controller.running:
        controller.play()
        process.update()

print(f'Started in {time.time() - t0} seconds')
del t0

if __name__ == '__main__':
    controller.goto_scene(controller.scenes.main_menu)
    main()
