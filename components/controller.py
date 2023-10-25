import pygame
import components.events as events
import components.scenes as scenes
from constants import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class CursorManager():
    default_cursor = pygame.SYSTEM_CURSOR_ARROW

    def set(self, value: int):
        pygame.mouse.set_cursor(value)

    def arrow(self):
        self.set(pygame.SYSTEM_CURSOR_ARROW)

    def crosshair(self): # 準星
        self.set(pygame.SYSTEM_CURSOR_CROSSHAIR)

    def hand(self):
        self.set(pygame.SYSTEM_CURSOR_HAND)

    def ibeam(self): # 預備輸入的光標
        self.set(pygame.SYSTEM_CURSOR_IBEAM)

    def sizeall(self): # 移動
        self.set(pygame.SYSTEM_CURSOR_SIZEALL)

    def default(self):
        self.set(self.default_cursor)

class Controller():
    running = True

    screen = screen
    events = events
    scenes = scenes

    cursor = CursorManager()

    # 創建視窗渲染時鐘
    clock = pygame.time.Clock()

    current_scene: scenes.Scene = None

    def __init__(self):
        pass
    
    __visited: set[scenes.Scene] = set()

    def goto_scene(self, scene: scenes.Scene):
        if scene not in self.__visited:
            scene.init()
            self.__visited.add(scene)
        self.current_scene = scene

    def play(self):
        # 設置更新幀數
        self.clock.tick(FPS)

        events.event_manager.init()
        # 讀取使用者的活動
        for event in pygame.event.get():
            # 退出遊戲
            if event.type == pygame.QUIT:
                self.running = False
            events.event_manager.handle(event)

        # 繪製當前場景
        if self.current_scene is not None:
            self.current_scene.play()

        # 更新視窗
        pygame.display.flip()

controller = Controller()
