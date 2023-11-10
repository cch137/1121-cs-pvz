import typing
import utils.asynclib as asynclib
import components.events as events

T = typing.TypeVar('T')

class Ref(typing.Generic[T]):
    def __init__(self, value: T):
        self.__value = value
        self.__targets: set[events.EventTarget] = set()
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        for target in tuple(self.__targets):
            asynclib.run_threads(lambda: target.dispatch_event(events.RefChangeEvent(target)))

    def __str__(self) -> str:
        return str(self.value)

    def bind(self, target: events.EventTarget):
        self.__targets.add(target)
    
    def unbind(self, target: events.EventTarget):
        self.__targets.remove(target)

class Computed(Ref[T], events.EventTarget):
    def __init__(self, getter: typing.Callable[[], T], *related_refs: Ref):
        Ref.__init__(self, getter())
        events.EventTarget.__init__(self)
        self.__getter = getter
        self.__related_refs = set()
        self.add_related_refs(*related_refs)
        self.add_event_listener(events.REF_CHANGE, lambda: self.compute())
    
    @property
    def value(self):
        return Ref.value.fget(self)

    @value.setter
    def value(self, value):
        raise 'Computed is read only'

    def add_related_refs(self, *refs: Ref):
        for ref in refs:
            self.__related_refs.add(ref)
            ref.bind(self)

    def remove_related_refs(self, *refs: Ref):
        for ref in refs:
            self.__related_refs.remove(ref)
            ref.unbind(self)

    def compute(self):
        Ref.value.fset(self, self.__getter())

def to_ref(value: Ref[T] | T) -> Ref[T]:
    return value if isinstance(value, Ref) else Ref(value)
