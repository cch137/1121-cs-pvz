from typing import Callable, Any
import time
import threading

def is_asyncfunc(func: Callable):
    return bool(func.__code__.co_flags & 0x80)

async def wrapper(callback: Callable, *args):
    if is_asyncfunc(callback):
        return await callback(*args)
    return callback(*args)

__index = 0
__runnings: dict[int, bool] = {}

def __create_index():
    global __index
    __index += 1
    __runnings[__index] = True
    return __index

def __delete_index(index: int):
    del __runnings[index]

def __is_running(index: int):
    return index in __runnings

def run_threads(*callbacks: Callable):
    for callback in callbacks:
        threading.Thread(target=callback).start()

def set_timeout(callback: Callable, milliseconds: float, *args: Any) -> int:
    '''
    callback 將在等待 timeoutSecs 後被執行。\\
    在任務執行前可用 clear_timeout 取消定時任務。\\
    函式返會任務 id。

    參數：\\
    callback - 須調用的函式 \\
    timeoutSecs - 須等待的秒數 \\
    *args - 須傳入 callback 的參數
    '''
    task_id = __create_index()
    def _callback():
        if __is_running(task_id):
            try:
                callback(*args)
            except Exception as e:
                print(e)
            finally:
                __delete_index(task_id)
    threading.Timer(max(0, milliseconds), _callback).start()
    return task_id

def set_interval(callback: Callable, milliseconds: float, *args: Any) -> int:
    '''
    callback 將以 intervalSecs 為間隔循環執行。\\
    在任務執行前可用 clear_interval 取消定時任務。\\
    函式返會任務 id。

    參數：\\
    callback - 須調用的函式 \\
    intervalSecs - 執行間隔的描述 \\
    *args - 須傳入 callback 的參數
    '''
    task_id = __create_index()
    def _callback():
        next_execute_t = time.time()
        while True:
            now = time.time()
            next_execute_t += milliseconds
            time.sleep(max(0, next_execute_t - now))
            if __is_running(task_id):
                try:
                    callback(*args)
                except Exception as e:
                    print(e)
            else:
                break
    threading.Thread(target=_callback).start()
    return task_id

clear_timeout: Callable[[int], None] = lambda task_id: __delete_index(task_id)
clear_interval = clear_timeout
