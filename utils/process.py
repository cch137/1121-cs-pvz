import os
import shutil
import time
import pygame

def clear_caches():
    '''非必要功能：移除緩存資料夾'''
    for dirpath, folders, files in os.walk('.'):
        for folder in folders:
            if folder != '__pycache__': continue
            try: shutil.rmtree(dirpath + '\\' + folder + '\\')
            except: pass

class FPSCounter():
    recorded_time = 0
    fps = 0

    def reset(self, value = 0):
        self.fps = value

    def count(self):
        self.fps += 1

    def show(self):
        if self.fps:
            print(f'FPS: {self.fps}')

    def run(self):
        now = int(timestamp)
        if self.recorded_time != now:
            self.show()
            self.reset(1)
            self.recorded_time = now
        else:
            self.count()

fps_counter = FPSCounter()

timestamp: float = 0
ticks: int = 0

def update():
    global timestamp
    global ticks
    timestamp = time.time()
    ticks = pygame.time.get_ticks()
    fps_counter.run()
