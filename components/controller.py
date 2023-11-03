import os
import io
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

def _resolve_asset_filepath(fp: str):
    if ASSETS_DIRNAME in fp: return fp
    return os.path.join(ASSETS_DIRNAME, *fp.replace('\\', '/').split('/'))

class PreloadSound():
    def __init__(self, asset_filepath: str, volume: float = 1) -> None:
        self.fp = _resolve_asset_filepath(asset_filepath)
        self.sounds: dict[float,pygame.mixer.Sound] = dict()
        self.load(volume)
    
    def load(self, volume: float = 1):
        if volume not in self.sounds:
            self.sounds[volume] = pygame.mixer.Sound(self.fp)
            self.sounds[volume].set_volume(volume)
        return self.sounds[volume]

class PreloadImage():
    def __init__(self, asset_filepath: str) -> None:
        self.fp = _resolve_asset_filepath(asset_filepath)
        self.bytes = open(self.fp, 'rb').read()
    
    def load(self, size: tuple[int,int] | None = None):
        image = pygame.image.load(io.BytesIO(self.bytes))
        if size is not None:
            image = pygame.transform.scale(image, size)
        return image

class PreloadAnimation():
    def __init__(self, asset_filepath: str, frames: int, format: str = 'png') -> None:
        self.fp = _resolve_asset_filepath(asset_filepath)
        self.images = tuple(PreloadImage(f'{self.fp}_{i}.{format}') for i in range(1, frames + 1))
    
    def load(self, durationSecs: float, size: tuple[int,int] = None):
        return elong_list([i.load(size) for i in self.images], int(FPS * durationSecs))

class MediaManager():
    def __init__(self):
        self.sounds: dict[str,PreloadSound] = dict()
        self.images: dict[str,PreloadImage] = dict()
        self.animations = dict[str,PreloadAnimation]()
    
    def preload_sound(self, asset_filepath: str):
        asset_filepath = _resolve_asset_filepath(asset_filepath)
        if asset_filepath not in self.sounds:
            self.sounds[asset_filepath] = PreloadSound(asset_filepath)
        return self.sounds[asset_filepath]
    
    def preload_image(self, asset_filepath: str):
        asset_filepath = _resolve_asset_filepath(asset_filepath)
        if asset_filepath not in self.images:
            self.images[asset_filepath] = PreloadImage(asset_filepath)
        return self.images[asset_filepath]
    
    def preload_animation(self, asset_filepath: str, frames: int, format: str = 'png'):
        asset_filepath = _resolve_asset_filepath(asset_filepath)
        if asset_filepath not in self.animations:
            self.animations[asset_filepath] = PreloadAnimation(asset_filepath, frames, format)
        return self.animations[asset_filepath]
    
    def preload_all_images(self):
        for dirname, dirnames, filenames in os.walk(ASSETS_DIRNAME):
            for filename in filenames:
                fp = f'{dirname}/{filename}'
                if utils.media.determine_file_type(fp)[0] == 'image':
                    try: self.preload_image(fp)
                    except: pass
    
    def load_sound(self, asset_filepath: str, volume: float = 1):
        return self.preload_sound(asset_filepath).load(volume)
    
    def load_image(self, asset_filepath: str, size: tuple[int,int] | None = None):
        return self.preload_image(asset_filepath).load(size)
    
    def load_animation(self, asset_filepath: str, duration_secs: float, size: tuple[int,int] | None = None, frames: int | None = None, format: str = 'png'):
        return self.preload_animation(asset_filepath, frames, format).load(duration_secs, size)

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
        self.media.preload_all_images()
        self.clock = pygame.time.Clock() # 渲染時鐘
        self.__visited = set()

    def goto_scene(self, scene: scenes.Scene):
        self.current_scene = scene
        if scene not in self.__visited:
            scene.init()
            self.__visited.add(scene)
        if scene.background_music_fp is not None:
            try:
                pygame.mixer.music.load(scene.background_music_fp)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(scene.background_music_volume)
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
