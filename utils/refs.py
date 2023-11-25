from typing import Any, TypeVar, Generic, Set, Callable
import utils.asynclib as asynclib
import components.events as events

T = TypeVar('T')

class Ref(Generic[T], events.EventTarget):
    __targets: Set[events.EventTarget] | None = None
    
    def __init__(self, value: T):
        self.__value = value

    @property
    def value(self) -> T:
        return self.__value

    @value.setter
    def value(self, value: T):
        self.__value = value
        if self.__targets is None: return
        asynclib.run_threads(lambda: tuple(target.dispatch_event(events.RefChangeEvent(target)) for target in (self, *self.__targets)))

    def __str__(self) -> str:
        return str(self.__value)

    def bind(self, target: events.EventTarget):
        if self.__targets is None:
            self.__targets = set()
        self.__targets.add(target)

    def unbind(self, target: events.EventTarget):
        if self.__targets is not None:
            self.__targets.remove(target)

class Computed(Ref[T], events.EventTarget):
    bound_refs: Set[Ref] | None = None

    def __init__(self, getter: Callable[[], T], *related_refs: Ref):
        Ref.__init__(self, getter())
        self.getter = getter
        self.bind_refs(*related_refs)

    @property
    def value(self):
        return Ref.value.fget(self)

    @value.setter
    def value(self, value: T):
        raise 'Computed is read only'

    def bind_refs(self, *refs: Ref):
        if len(refs) == 0:
            return
        if self.bound_refs is None:
            self.bound_refs = set()
            self.add_event_listener(events.REF_CHANGE, self.compute)
        for ref in refs:
            ref.bind(self)
            self.bound_refs.add(ref)

    def unbind_refs(self, *refs: Ref):
        for ref in refs:
            ref.unbind(self)
            self.bound_refs.remove(ref)
        if len(self.bound_refs) == 0:
            self.bound_refs = None
            self.remove_event_listener(events.REF_CHANGE, self.compute)

    def compute(self):
        Ref.value.fset(self, self.getter())
        asynclib.run_threads(lambda: self.dispatch_event(events.ChangeEvent(self)))

def is_ref(value: Ref[T] | T) -> bool:
    return isinstance(value, Ref)

def to_ref(value: Ref[T] | T) -> Ref[T]:
    return value if isinstance(value, Ref) else Ref(value)

def to_value(value: Ref[T] | T) -> T:
    return value.value if isinstance(value, Ref) else value
