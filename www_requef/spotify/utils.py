from functools import wraps
from time import time
from asyncio import iscoroutinefunction


def cache_result(timeout_s: float):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key not in cache or cache[key][1] + timeout_s < time():
                cache[key] = (func(*args, **kwargs), time())
            return cache[key][0]

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key not in cache or cache[key][1] + timeout_s < time():
                cache[key] = (await func(*args, **kwargs), time())
            return cache[key][0]

        return async_wrapper if iscoroutinefunction(func) else wrapper

    return decorator
