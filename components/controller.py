import pygame
import components
from constants import *

class CursorManager():
    default_cursor = pygame.SYSTEM_CURSOR_ARROW

    def set(self, value: int):
        pygame.mouse.set_cursor(value)

    def hand(self):
        self.set(pygame.SYSTEM_CURSOR_HAND)

    def arrow(self):
        self.set(pygame.SYSTEM_CURSOR_ARROW)

    def default(self):
        self.set(self.default_cursor)

class Controller():
    running = True

    screen = components.screen

    cursor = CursorManager()

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
