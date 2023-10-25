import pygame
import components
from constants import *

class Controller():
    running = True

    screen = components.screen

    # 創建視窗渲染時鐘
    clock = pygame.time.Clock()

    current_scene: components.scene.Scene = None

    def __init__(self):
        pass
    
    def goto_scene(self, scene: components.scene.Scene):
        self.current_scene = scene
    
    def play(self):
        # 設置更新幀數
        self.clock.tick(FPS)

        components.event_manager.init()
        # 讀取使用者的活動
        for event in pygame.event.get():
            # 退出遊戲
            if event.type == pygame.QUIT:
                self.running = False
            components.event_manager.handle(event)

        # 繪製當前場景
        if self.current_scene is not None:
            self.current_scene.play()

        # 更新視窗
        pygame.display.flip()

controller = Controller()
