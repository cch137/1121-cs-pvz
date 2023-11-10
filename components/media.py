import os
import io
import pygame
import utils.media
from typing import Dict
from utils.constants import *
from utils.elong_list import elong_list

def _resolve_asset_filepath(fp: str):
    if ASSETS_DIRNAME in fp: return os.path.abspath(fp)
    return os.path.abspath(os.path.join(ASSETS_DIRNAME, *fp.replace('\\', '/').split('/')))

class PreloadSound():
    def __init__(self, asset_filepath: str, volume: float = 1) -> None:
        self.fp = _resolve_asset_filepath(asset_filepath)
        self.sounds: Dict[float,pygame.mixer.Sound] = dict()
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
    
    def load(self, size: Coordinate | int | None = None):
        image = pygame.image.load(io.BytesIO(self.bytes))
        if size is not None:
            image = pygame.transform.scale(image, (size, size) if type(size) is int else size)
        return image

class PreloadAnimation():
    def __init__(self, asset_filepath: str, frames: int, format: str = 'png') -> None:
        self.fp = _resolve_asset_filepath(asset_filepath)
        self.images = tuple(PreloadImage(f'{self.fp}_{i}.{format}') for i in range(1, frames + 1))
    
    def load(self, durationSecs: float, size: Coordinate | int = None):
        return elong_list([i.load(size) for i in self.images], int(FPS * durationSecs))

class MediaManager():
    def __init__(self):
        self.sounds: Dict[str,PreloadSound] = dict()
        self.images: Dict[str,PreloadImage] =  dict()
        self.animations: Dict[str,PreloadAnimation] = dict()
    
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
        '''動畫圖片命名格式例子：anim_1.png, anim_2.png, ..., anim_10.png （假設圖片放置在 assets 目錄）
        
        函式使用例子：load_animation('assets/anim', 10, 1.5, (60, 60))'''
        asset_filepath = _resolve_asset_filepath(asset_filepath)
        if asset_filepath not in self.animations:
            self.animations[asset_filepath] = PreloadAnimation(asset_filepath, frames, format)
        return self.animations[asset_filepath]
    
    def preload_assets(self, images: bool = True, audio: bool = False):
        for dirname, dirnames, filenames in os.walk(ASSETS_DIRNAME):
            for filename in filenames:
                fp = f'{dirname}/{filename}'
                match utils.media.determine_file_type(fp)[0]:
                    case 'image':
                        try:
                            if images:
                                self.preload_image(fp)
                        except:
                            pass
                    case 'audio':
                        try:
                            if audio:
                                self.preload_sound(fp)
                        except:
                            pass
    
    def load_sound(self, asset_filepath: str, volume: float = 1):
        return self.preload_sound(asset_filepath).load(volume)
    
    def load_image(self, asset_filepath: str, size: Coordinate | int | None = None):
        return self.preload_image(asset_filepath).load(size)
    
    def load_animation(self, asset_filepath: str, duration_secs: float, size: Coordinate | int | None = None, frames: int | None = None, format: str = 'png'):
        return self.preload_animation(asset_filepath, frames, format).load(duration_secs, size)

media = MediaManager()
