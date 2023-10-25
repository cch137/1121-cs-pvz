import pygame
from constants import *
import utils.process as process
from components import screen, event_manager, Scene

# 設置視窗圖標、標題，然後初始化視窗
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption(TITLE)
pygame.init()

# 創建視窗渲染時鐘
clock = pygame.time.Clock()

process.clear_caches()

def main(testing_scene: Scene | None = None):
    while True:
        # 設置更新幀數
        clock.tick(FPS)

        event_manager.init()
        # 讀取使用者的活動
        for event in pygame.event.get():
            # 退出遊戲
            if event.type == pygame.QUIT: return
            event_manager.handle(event)

        if testing_scene != None:
            testing_scene.update()
            testing_scene.compose()
            testing_scene.draw()

        # 更新視窗
        pygame.display.flip()

        # 更新 FPS 統計器
        process.fps_counter.run()

# main()
