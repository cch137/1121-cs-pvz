import os
import pygame
import components.events as events
import components.scenes as scenes
from constants import *
import utils.media
from utils.elong_list import elong_list

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

assets_dirname = 'assets'

def __resolve_asset_filepath(fp: str):
    return os.path.join(assets_dirname, *fp.replace('\\', '/').split('/'))

class PreloadAsset():
    def __init__(self, asset_filepath: str) -> None:
        self.fp = __resolve_asset_filepath(asset_filepath)
        self.bytes = open(self.fp, 'rb').read()

class PreloadImage(PreloadAsset):
    def __init__(self, asset_filepath: str) -> None:
        PreloadAsset.__init__(self, asset_filepath)
        self.size = utils.media.get_image_size(self.fp)
        self.format = utils.media.get_image_channels(self.fp)
    
    def load(self, size):
        return pygame.image.frombytes(self.bytes, self.size, self.format)

class PreloadAnimation():
    def __init__(self, asset_filepath: str) -> None:
        self.images: tuple[PreloadImage] = tuple()
    
    def load(self, size):
        return elong_list

class MediaManager():
    def __init__(self):
        self.audios = dict()
        self.images: dict[str,PreloadImage] = dict()
        self.animations = dict()
    
    def preload_asset(self, asset_filepath: str):
        return PreloadAsset(asset_filepath)
    
    def preload_all_assets(self):
        for dirname, dirnames, filenames in os.walk(assets_dirname):
            for filename in filenames:
                self.preload_asset(f'{dirname}/{filename}')

class Controller():
    current_scene: scenes.Scene
    __visited: set[scenes.Scene]

    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.events = events
        self.scenes = scenes
        self.cursor = CursorManager()
        self.media = MediaManager()
        self.media.preload_all_assets()
        self.clock = pygame.time.Clock() # 渲染時鐘
        self.__visited = set()

    def goto_scene(self, scene: scenes.Scene):
        self.current_scene = scene
        if scene not in self.__visited:
            scene.init()
            self.__visited.add(scene)

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
