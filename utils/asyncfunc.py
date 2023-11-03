import typing

def is_asyncfunc(func: typing.Callable):
    return bool(func.__code__.co_flags & 0x80)

async def wrapper(listener: typing.Callable, *args):
    if is_asyncfunc(listener):
        return await listener(*args)
    return listener(*args)
