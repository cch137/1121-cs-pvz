import os
import shutil
import time

def clear_caches():
    '''非必要功能：移除緩存資料夾'''
    for dirpath, folders, files in os.walk('.'):
        for folder in folders:
            if folder != '__pycache__': continue
            try: shutil.rmtree(dirpath + '\\' + folder + '\\')
            except: pass

class FPSCounter():
    recorded_time = 0
    fps = 60

    def reset(self, value = 0):
        self.fps = value

    def count(self):
        self.fps += 1

    def show(self):
        print(f'FPS: {self.fps}')

    def run(self):
        now = self.now()
        if self.recorded_time != now:
            self.show()
            self.recorded_time = now
            self.reset(1)
        else:
            self.count()

    def now(self):
        return int(time.time())

fps_counter = FPSCounter()
