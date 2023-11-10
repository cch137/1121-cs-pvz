import typing
import pygame

T = typing.TypeVar('T')

class Ref(typing.Generic[T]):
    def __init__(self, value: T):
        import components.element as element
        self.__value = value
        self.__textboxes: set[element.TextBox] = set()
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        import components.events as events
        self.__value = value
        for tx in self.__textboxes:
            tx.dispatch_event(events.ChangeEvent(tx))

    def __str__(self) -> str:
        return str(self.value)

    def bind(self, textbox):
        self.__textboxes.add(textbox)
    
    def unbind(self, textbox):
        self.__textboxes.remove(textbox)

def to_ref(value: Ref[T] | T) -> Ref[T]:
    return value if isinstance(value, Ref) else Ref(value)
