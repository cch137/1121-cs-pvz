from typing import *
from utils.constants import *
import utils.refs as refs
import components.entities as entities
import components.entities.plants as plants
import components.entities.zombies as zombies
import components.element as element
import components.events as events
import components.scenes as scenes

class GameMap():
    def __init__(self):
        pass

    def get_tile(self, row: int, col: int) -> element.Element:
        pass

    def get_row_bottom(self, row: int) -> int:
        '''取得 row 的地平線'''
        # 未完成！
        return 0

class Level(element.Element):
    ticks: int
    suns: int
    get_row_bottom: Callable[[], int]
    map: GameMap

class Spawner():
    def __init__(self, schedule_tick: int, *entities: entities.Entity):
        self.schedule = schedule_tick
        self.entities = entities
        self.__used = False

    @property
    def entity(self):
        return self.entities[0]

    def is_spawnable(self, level: Level):
        return not self.__used and self.schedule <= level.ticks

    def spawn(self, level: Level):
        if self.__used:
            raise 'Spawner has been used'
        self.__used = True
        level.scene.add_element(*self.entities)
    
    def kill(self, *args: Any, **kwargs: Any):
        self.__used = True
        for entity in self.entities:
            entity.kill(*args, **kwargs)

class SunSpawner(Spawner):
    def __init__(self, schedule_tick: int = 0, x_range: Tuple[int, int] = (100, 980), y_range: Tuple[int, int] = (200, 700), value=25):
        Spawner.__init__(self, schedule_tick, entities.Sun(x_range, y_range, value))

    def spawn(self, level: Level):
        Spawner.spawn(self, level)
        self.entity.add_event_listener(events.CLICK_R, lambda: level.eval_suns(self.entity.kill()))

class ZombieSpawner(Spawner):
    def __init__(self, schedule_tick: int, row: int, *zombies: zombies.Zombie):
        self.row = row
        Spawner.__init__(self, schedule_tick, *zombies)

    def spawn(self, level: Level):
        Spawner.spawn(self, level)
        for i, zombie in enumerate(self.entities):
            zombie.rect.bottomleft = (WINDOW_WIDTH + i * ZOMBIES_GAP, level.map.get_row_bottom(self.row))

class Level(element.Element):
    def __init__(self, spawners: Iterable[Spawner] = tuple()):
        '''遊戲關卡'''
        element.Element.__init__(self, (0, 0))
        self.spawners = set(spawners)
        self.ticks = 0
        self.map = GameMap()
        self.__suns = refs.Ref(0)
        self.victory = refs.Ref(True)
    
    def is_growable_tile(self, row: int, col: int):
        return len(self.map.get_tile(row, col).children) == 0

    def grow_plant(self, plant: plants.Plant, row: int, col: int):
        '''種植一個植物到 tile，成功種植植物時返回 Ture，否則 Fasle。種植失敗時執行 plant.kill()'''
        if self.is_growable_tile(row, col):
            self.map.get_tile(row, col).append_child(plant)
            return True
        plant.kill()
        return False

    @property
    def suns(self):
        return self.__suns

    def has_suns(self, value: int):
        '''判斷是否有足夠的太陽數量'''
        return self.__suns.value >= value

    def eval_suns(self, value: int = 0):
        '''對太陽數量進行運算'''
        if value != 0:
            self.__suns.value += value
            self.dispatch_event(events.SunsChangeEvent(self))

    def update(self, *args: Any, **kwargs: Any) -> None:
        for spawner in self.spawners:
            if spawner.is_spawnable(self):
                spawner.spawn(self)
        self.ticks += 1

    def bind(self, scene: scenes.Scene):
        scene.add_element(self)

    def unbind(self, scene: scenes.Scene):
        scene.remove_element(self)
