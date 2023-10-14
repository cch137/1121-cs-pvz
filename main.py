import pygame
from constants import *
from utils.files import *
from components import screen, event_manager

# 用於控制程序視窗，只要為 True，程序視窗就會一直被渲染
running = True

# 設置視窗 icon
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
# 設置視窗標題
pygame.display.set_caption(TITLE)
# pygame 初始化
pygame.init()

# 創建視窗渲染時鐘
clock = pygame.time.Clock()

clear_caches()

def main():
    while True:
        # 設置更新幀數
        clock.tick(FPS)

        event_manager.init()
        # 讀取使用者的活動
        for event in pygame.event.get():
            # 退出遊戲
            if event.type == pygame.QUIT: return
            event_manager.handle(event)

        # 設定視窗背景顏色
        screen.fill(BACKGROUND_COLOR)

        # 更新視窗
        pygame.display.flip()

main()
