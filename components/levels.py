from typing import *
from utils.constants import *
from components.entities import Entity, Element, Sun
import components.events as events
import components.scenes as scenes
import utils.refs as refs
import utils.asynclib as asynclib

class Level(Element):
    ticks: int
    suns: int

class Spawner():
    def __init__(self, schedule_tick: int, *entities: Entity):
        self.schedule = schedule_tick
        self.entities = entities
        self.__used = False
    
    def is_spawnable(self, level: Level):
        return not self.__used and self.schedule <= level.ticks
    
    def spawn(self, level: Level):
        if self.__used:
            raise 'Spawner has been used'
        self.__used = True
        level.scene.add_element(*self.entities)

class SunSpawner(Spawner):
    def __init__(self, schedule_tick: int = 0):
        self.sun = Sun()
        Spawner.__init__(self, schedule_tick, self.sun)
    
    def spawn(self, level: Level):
        Spawner.spawn(self, level)
        self.sun.add_event_listener(events.CLICK, lambda: level.eval_suns(self.sun.kill()))

class Level(Element):
    def __init__(self, spawners: Iterable[Spawner] = tuple()):
        Element.__init__(self, (0, 0))
        self.spawners = set(spawners)
        self.ticks = 0
        self.__suns = refs.Ref(0)
        _self = self
        class SunsChangeEvent(events.UserEvent):
            def __init__(self):
                events.UserEvent.__init__(self, events.SUN_CHANGES, _self)
        self.events = { events.SUN_CHANGES: SunsChangeEvent }
    
    @property
    def suns(self):
        return self.__suns
    
    def has_suns(self, value: int):
        return self.__suns.value >= value
    
    def eval_suns(self, value: int = 0):
        if value != 0:
            self.__suns.value += value
            asynclib.run_threads(lambda: self.dispatch_event(self.events[events.SUN_CHANGES]()))
    
    def update(self, *args: Any, **kwargs: Any) -> None:
        Element.update(self, *args, **kwargs)
        for spawner in self.spawners:
            if spawner.is_spawnable(self):
                spawner.spawn(self)
        self.ticks += 1

    def bind(self, scene: scenes.Scene):
        scene.add_element(self)

    def unbind(self, scene: scenes.Scene):
        scene.remove_element(self)
