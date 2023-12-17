from typing import *
from random import randint
from typing import Any
from utils.constants import *
import utils.asynclib as asynclib
import utils.refs as refs
import components.entities as entities
import components.entities.plants as plants
import components.entities.zombies as zombies
import components.element as element
import components.events as events
import components.scenes as scenes
from components.media import media

class Level(element.Element):
    ticks: int
    suns: int

class Spawner():
    def __init__(self, schedule_tick: int, *entities: entities.Entity):
        self.schedule = schedule_tick
        self.entities = entities
        self.is_used = False

    @property
    def entity(self):
        return self.entities[0]

    def is_spawnable(self, level: Level):
        return not self.is_used and self.schedule <= level.ticks

    def spawn(self, level: Level):
        if self.is_used:
            raise 'Spawner has been used'
        self.is_used = True
        level.scene.add_element(*self.entities)
    
    def kill(self, *args: Any, **kwargs: Any):
        self.is_used = True
        for entity in self.entities:
            entity.kill(*args, **kwargs)

class ZombieSpawner(Spawner):
    def __init__(self, schedule_tick: int, row: int, *zombies: zombies.Zombie):
        self.row = row
        Spawner.__init__(self, max(1, schedule_tick), *zombies)

    def spawn(self, level: Level):
        for i, zombie in enumerate(self.entities):
            zombie.rect.bottomleft = (WINDOW_WIDTH + i * ZOMBIES_GAP, level.get_row_bottom(self.row, -15))
        Spawner.spawn(self, level)

class Tile(element.Element):
    grow_type: type[plants.Plant] | None = None

    def __init__(self, size: Coordinate, r: int, c: int):
        element.Element.__init__(self, size)
        self.id = f'tile-{r}-{c}'
        self.max_width = size[0]
        self.max_height = size[1]
        self.background_color = (0, 0, 0, 0)
        self.justify_content = CENTER
        self.align_items = CENTER
        if r % 2 == 0:
            self.background_color = TILE_BG_1 if c % 2 == 0 else TILE_BG_2
        else:
            self.background_color = TILE_BG_3 if c % 2 == 0 else TILE_BG_4

    @property
    def plant(self):
        for child in self.children:
            if isinstance(child, plants.Plant):
                return child
        return None

    @property
    def growable(self):
        return self.plant is None

    def grow(self, plant: plants.Plant):
        if not self.growable:
            raise 'Tile is not growable'
        self.append_child(plant)
        return plant

    def update(self):
        if self.grow_type is not None:
            plant = self.grow_type()
            self.grow(plant)
            self.grow_type = None
            controller.level.add_suns(-plant.price)

class Level(element.Element):
    def __init__(self, scene: scenes.Scene, spawners: Iterable[Spawner] = tuple()):
        '''遊戲關卡'''
        level = self
        element.Element.__init__(self, (0, 0))
        scene.add_element(self)

        self.spawners = set(spawners)
        self.ticks = 0
        self.__last_sun_drop = 0
        self.sun_drop_frequency_ticks = 300

        self.suns = refs.Ref(0)
        self.suns.add_event_listener(events.REF_CHANGE, lambda: self.dispatch_event(events.SunsChangeEvent(self)))
        self.waiting_for_victory: bool = False
        self.__victory = refs.Ref(False)
        
        self.tiles = tuple(tuple(Tile(TILE_SIZE, r, c) for c in range(MAP_COLUMNS)) for r in range(MAP_ROWS))
        self.__rows = tuple(element.Element(None, ROW, r) for r in self.tiles)
        self.game_map = element.Element(None, None, self.__rows)
        self.game_map.compose()
        scene.add_element(self.game_map)

        class Card(element.Element):
            price: int
            selected: bool = False
            mask: element.Element | None = None

            def __init__(self, image: pygame.Surface, plant_type: type[plants.Plant]):
                element.Element.__init__(self)
                self.price = plant_type().price
                self.plant_type = plant_type
                plant_image_el = element.Element(image)
                plant_image_el.max_height = 100
                self.append_child(plant_image_el)
                self.append_child(element.TextBox(self.price, 20))
                self.max_width = 100
                self.max_height = 150
                self.padding = (8, 6, 4)
                self.spacing = 10
                self.background_color = (0, 0, 0, 127)
                self.compose()
                def _click():
                    for card in level.cards:
                        card.selected = card is self and not card.selected
                self.add_event_listener(events.CLICK, _click)
            
            def update(self):
                if level.has_suns(self.price):
                    if self.mask is not None:
                        self.cursor = 'hand'
                        self.mask.kill()
                        self.mask = None
                else:
                    if self.selected:
                        self.selected = False
                    if self.mask is None:
                        self.mask = element.Element(self.rect.size)
                        self.mask.background_color = (0, 0, 0, 127)
                        self.mask.z_index = 99
                        scene.add_element(self.mask)
                        self.cursor = None
                if self.mask is not None:
                    self.mask.rect.center = self.rect.center
                self.background_color = (60, 50, 30) if self.selected else (48, 30, 24)

        self.cards = tuple(Card(i, p) for i, p in (
            (media.load_image('plants/sunflower.png', CARD_IMAGE_SIZE), plants.SunFlower),
            (media.load_image('plants/peashooter.png', CARD_IMAGE_SIZE), plants.PeaShooter),
            (media.load_image('plants/gatlingpea.png', CARD_IMAGE_SIZE), plants.GatlingPea),
            (media.load_image('plants/snowpea.png', CARD_IMAGE_SIZE), plants.SnowPea),
            (media.load_image('plants/wallnut.png', CARD_IMAGE_SIZE), plants.WallNut),
            (media.load_image('plants/potatomine.png', CARD_IMAGE_SIZE), plants.PotatoMine),
        ))
        span1 = element.Element((8, 8))
        span2 = element.Element((8, 8))
        span1.background_color = (0, 0, 0, 0)
        span2.background_color = (0, 0, 0, 0)
        self.card_board = element.Element(None, ROW, [
            element.Element(None, None, [
                span1,
                element.Element(media.load_image('entities/sun.png', (CARD_IMAGE_SIZE[0] * 0.8, CARD_IMAGE_SIZE[1] * 0.8))),
                span2,
                element.TextBox(self.suns)
            ]),
            element.Element(0),
            *self.cards
        ])
        self.card_board.padding = 10
        self.card_board.spacing = 8
        self.card_board.background_color = (65, 60, 45)
        self.card_board.compose()
        scene.add_element(self.card_board)

    def get_row_bottom(self, row: int, pad: int):
        return self.__rows[row].rect.bottom - pad

    def get_tile(self, row: int, col: int):
        return self.scene.get_element_by_id(f'tile-{row}-{col}')

    @property
    def victory(self) -> bool:
        return self.__victory.value
    
    @victory.setter
    def victory(self, value: bool):
        self.__victory.value = value
    
    @property
    def selected_plant(self):
        for card in self.cards:
            if card.selected:
                return card.plant_type
        return None

    def has_suns(self, value: int):
        '''判斷是否有足夠的太陽數量'''
        return self.suns.value >= value

    def add_suns(self, value: int = 0):
        '''對太陽數量進行加法運算'''
        self.suns.value += value

    def drop_sun(self):
        map_rect = self.game_map.rect
        sun = entities.Sun()
        self.scene.add_element(sun)
        sun.rect.center = (randint(map_rect.left, map_rect.right), -sun.rect.height / 2)
        sun.move_limit = int(sun.rect.height / 2 + randint(map_rect.top, map_rect.bottom))

    def update(self):
        if len(zombies.all_zombies) == 0 and len(self.spawners) == 0:
            if not self.waiting_for_victory:
                self.waiting_for_victory = True
                def the_end():
                    if not self.waiting_for_victory:
                        return
                    self.victory = True
                    controller.unload_sceen(controller.scenes.main_game)
                    controller.goto_scene(controller.scenes.the_end)
                asynclib.set_timeout(the_end, 3000)
        elif self.waiting_for_victory:
            self.waiting_for_victory = False

        if self.__last_sun_drop + self.sun_drop_frequency_ticks < self.ticks:
            self.__last_sun_drop = self.ticks
            self.drop_sun()
        for spawner in tuple(self.spawners):
            if spawner.is_spawnable(self):
                spawner.spawn(self)
            elif spawner.is_used:
                self.spawners.remove(spawner)
        selected_plant_type = self.selected_plant
        def grow_plant(_tile: Tile):
            def listener(e: events.ClickEvent):
                target_tile: Tile = e.target
                if _tile is target_tile and _tile.growable:
                    _tile.grow_type = selected_plant_type
                    for card in self.cards:
                        card.selected = False
            return listener
        for row in self.tiles:
            for tile in row:
                if tile.growable:
                    if selected_plant_type is not None:
                        tile.cursor = 'hand'
                        tile.add_event_listener(events.CLICK, grow_plant(tile))
                    else:
                        tile.cursor = None
                        tile.remove_event_listener(events.CLICK, remove_all=True)
        self.ticks += 1

from components import controller