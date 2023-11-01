from typing import Callable, Any
import time
import threading

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

def set_timeout(callback: Callable, timeoutSecs: float, *args: Any) -> int:
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
        time.sleep(max(0, timeoutSecs))
        if __is_running(task_id):
            try:
                callback(*args)
            except Exception as e:
                print(e)
            finally:
                __delete_index(task_id)
    threading.Thread(target=_callback, args=args).start()
    return task_id

def set_interval(callback: Callable, intervalSecs: float, *args: Any) -> int:
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
        while __is_running(task_id):
            now = time.time()
            next_execute_t += intervalSecs
            time.sleep(max(0, next_execute_t - now))
            if __is_running(task_id):
                try:
                    callback(*args)
                except Exception as e:
                    print(e)
    threading.Thread(target=_callback, args=args).start()
    return task_id

clear_timeout: Callable[[int], None] = lambda task_id: __delete_index(task_id)
clear_interval = clear_timeout