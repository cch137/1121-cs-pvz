import typing

def is_asyncfunc(func: typing.Callable):
    return bool(func.__code__.co_flags & 0x80)
