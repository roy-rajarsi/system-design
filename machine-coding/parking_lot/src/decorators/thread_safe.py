from threading import Lock
from typing import Any, Callable


def thread_safe(lock: Lock) -> Callable:

    def thread_safe_function_call(function: Callable) -> Callable:

        def thread_safe_function(*args, **kwargs) -> Any:
            lock.acquire(blocking=True, timeout=-1)
            result: Any = function(*args, **kwargs)
            lock.release()
            return result

        return thread_safe_function
    return thread_safe_function_call
