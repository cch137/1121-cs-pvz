from typing import *
from utils.constants import *
import utils.refs as refs
import components.entities as entities
import components.entities.plants as plants
import components.entities.zombies as zombies
import components.element as element
import components.events as events
import components.scenes as scenes

class Level(element.Element):
    ticks: int
    suns: int

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

class ZombieSpawner(Spawner):
    def __init__(self, schedule_tick: int, row: int, *zombies: zombies.Zombie):
        self.row = row
        Spawner.__init__(self, schedule_tick, *zombies)

    def spawn(self, level: Level):
        Spawner.spawn(self, level)
        for i, zombie in enumerate(self.entities):
            zombie.rect.bottomleft = (WINDOW_WIDTH + i * ZOMBIES_GAP, level.map.get_row_bottom(self.row))

class Tile(element.Element):
    def __init__(self, size: Coordinate, r: int, c: int):
        element.Element.__init__(self, size)
        self.id = f'tile-{r}-{c}'
        self.max_width = size[0]
        self.max_height = size[1]
        self.background_color = (0, 0, 0, 0)
        self.justify_content = CENTER
        self.align_items = CENTER
        def _mouseenter(): self.background_color = (255, 255, 255, 55)
        def _mouseleave(): self.background_color = (0, 0, 0, 0)
        self.add_event_listener(events.MOUSEENTER, _mouseenter)
        self.add_event_listener(events.MOUSELEAVE, _mouseleave)
    
    @property
    def plant(self):
        for child in self.children:
            if isinstance(child, plants.Plant):
                return child
    
    @property
    def growable(self):
        return not bool(self.plant)

    def grow(self, plant: plants.Plant):
        if not self.growable:
            raise 'Tile Not Growable'
        self.append_child(plant)

class Level(element.Element):
    def __init__(self, scene: scenes.Scene, spawners: Iterable[Spawner] = tuple()):
        '''遊戲關卡'''
        element.Element.__init__(self, (0, 0))
        scene.add_element(self)

        self.spawners = set(spawners)
        self.ticks = 0
        
        self.__tiles = tuple(tuple(Tile(TILE_SIZE, r, c) for c in range(MAP_COLUMNS)) for r in range(MAP_ROWS))
        self.__rows = tuple(element.Element(None, ROW, r) for r in self.__tiles)
        self.game_map = element.Element(None, None, self.__rows)
        self.game_map.compose()
        scene.add_element(self.game_map)

        self.suns = refs.Ref(0)
        self.suns.add_event_listener(events.REF_CHANGE, lambda: self.dispatch_event(events.SunsChangeEvent(self)))
        self.__victory = refs.Ref(False)

    def get_row_bottom(self, row: int, pad: int):
        return self.__rows[row].rect.bottom - pad

    def get_tile(self, row: int, col: int) -> Tile:
        return self.scene.get_element_by_id(f'tile-{row}-{col}')

    def grow_plant(self, plant: plants.Plant, row: int, col: int):
        self.get_tile(row, col).grow(plant)
        # '''種植一個植物到 tile，成功種植植物時返回 Ture，否則 Fasle。種植失敗時執行 plant.kill()'''
        # if self.is_growable_tile(row, col):
        #     self.map.get_tile(row, col).append_child(plant)
        #     return True
        # plant.kill()
        # return False

    @property
    def victory(self) -> bool:
        return self.__victory.value
    
    @victory.setter
    def victory(self, value: bool):
        self.__victory.value = value

    def has_suns(self, value: int):
        '''判斷是否有足夠的太陽數量'''
        return self.suns.value >= value

    def add_suns(self, value: int = 0):
        '''對太陽數量進行加法運算'''
        self.suns.value += value

    def drop_sun(self):
        map_rect = self.game_map.rect
        sun = entities.Sun((map_rect.left, map_rect.right), (map_rect.top, map_rect.bottom))
        sun.add_event_listener(events.CLICK_R, lambda: self.add_suns(sun.kill()))
        self.scene.add_element(sun)

    def update(self):
        for spawner in self.spawners:
            if spawner.is_spawnable(self):
                spawner.spawn(self)
        self.ticks += 1
