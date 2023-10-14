import pygame
from constants import *
from utils.files import *
from components.screen import screen

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

while running:
    # 設置更新幀數
    clock.tick(FPS)

    # 讀取使用者的活動
    for event in pygame.event.get():
        # 退出遊戲
        if event.type == pygame.QUIT:
            running = False
            break

    # 設定視窗背景顏色
    screen.fill(BACKGROUND_COLOR)

    # 更新視窗
    pygame.display.flip()

