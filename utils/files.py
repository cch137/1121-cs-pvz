import os
import shutil

def clear_caches():
    '''非必要功能：移除緩存資料夾'''
    for dirpath, folders, files in os.walk('.'):
        for folder in folders:
            if folder != '__pycache__': continue
            try: shutil.rmtree(dirpath + '\\' + folder + '\\')
            except: pass
