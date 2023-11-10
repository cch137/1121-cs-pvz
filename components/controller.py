import pygame
import components.events as events
import components.scenes as scenes
from typing import Set
from utils.constants import *
from components.media import media

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
    current_scene: scenes.Scene
    __visited: Set[scenes.Scene]

    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.events = events
        self.scenes = scenes
        self.cursor = CursorManager()
        self.media = media
        media.preload_assets()
        self.clock = pygame.time.Clock() # 渲染時鐘
        self.__visited = set()
        self.__playing_bg_music_fp: str | None = None
    
    def unload_sceen(self, scene: scenes.Scene):
        scene.kill()
        self.__visited.remove(scene)

    def goto_scene(self, scene: scenes.Scene):
        self.current_scene = scene
        if scene not in self.__visited:
            scene.init()
            self.__visited.add(scene)
        if scene.background_music is not None:
            try:
                if type(scene.background_music) is str:
                    if self.__playing_bg_music_fp == scene.background_music:
                        pygame.mixer.music.unpause()
                    else:
                        self.__playing_bg_music_fp = scene.background_music
                        pygame.mixer.music.load(scene.background_music)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(scene.background_music_volume)
                elif scene.background_music is True:
                    pygame.mixer.music.pause()
                else:
                    self.__playing_bg_music_fp = None
                    pygame.mixer.music.stop()
            except Exception as e:
                print(e)

    def play(self):
        # 設置更新幀數
        self.clock.tick(FPS)

        events.event_manager.setup()
        # 讀取使用者的活動
        for event in pygame.event.get():
            # 退出遊戲
            if event.type == pygame.QUIT:
                self.running = False
            # 處理事件
            events.event_manager.handle(event)

        # 繪製當前場景
        if self.current_scene is not None:
            self.current_scene.play()
        else: # 如果沒有場景，將 screen 填充為背景顏色
            self.screen.fill(BACKGROUND_COLOR)

        # 更新視窗
        pygame.display.flip()

controller = Controller()
