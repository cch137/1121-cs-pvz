from typing import Callable, Any
import time
import threading

def set_interval(callback: Callable, timeout: int, *args: Any):
    def _callback():
        time.sleep(timeout)
        callback(*args)
        set_timeout(_callback, timeout, *args)
    threading.Thread(target=_callback).start()

from utils.set_timeout import set_timeout
