from typing import Callable, Any
import time
import threading

def set_timeout(callback: Callable, timeout: int, *args: Any):
    def _callback():
        time.sleep(timeout)
        callback(*args)
    threading.Thread(target=_callback).start()
