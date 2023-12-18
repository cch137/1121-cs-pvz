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
    planter: plants.Planter | None = None

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

    def grow(self):
        if not self.growable:
            raise 'Tile is not growable'
        planter = self.planter
        if planter is None:
            raise 'Planter is not selected'
        self.append_child(planter.create())
        controller.level.add_suns(-planter.price)
        self.planter = None

    def update(self):
        if self.planter is not None:
            self.grow()

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
        self.__victory: refs.Ref[bool|None] = refs.Ref(None)
        
        self.tiles = tuple(tuple(Tile(TILE_SIZE, r, c) for c in range(MAP_COLUMNS)) for r in range(MAP_ROWS))
        self.__rows = tuple(element.Element(None, ROW, r) for r in self.tiles)
        self.game_map = element.Element(None, None, self.__rows)
        self.game_map.compose()
        scene.add_element(self.game_map)

        class Card(element.Element):
            selected: bool = False
            mask: element.Element | None = None

            def __init__(self, image: pygame.Surface, planter: plants.Planter):
                element.Element.__init__(self)
                self.planter = planter
                self.last_planted_lvl_ticks = -planter.cooldown_ticks
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
                def _click(e: events.ClickEvent):
                    for i in e.clicked_targets:
                        if isinstance(i, entities.Sun):
                            return
                    for card in level.cards:
                        card.selected = card is self and not card.selected and self.cd_percentage == 1 and level.has_suns(self.price)
                self.add_event_listener(events.CLICK, _click)
                mask1 = element.Element(self.rect.size)
                mask1.background_color = (0, 0, 0, 95)
                mask1.z_index = 99
                mask2 = element.Element((0, 0))
                mask2.background_color = (0, 0, 0, 95)
                mask2.z_index = 99
                def update():
                    mask1.rect.topleft = self.rect.topleft
                    mask1.background_color = (0, 0, 0, 0) if level.has_suns(self.price) else (0, 0, 0, 95 if self.cd_percentage < 1 else 127)
                    mask_height = mask1.rect.height * (1 - self.cd_percentage)
                    mask2.image = pygame.Surface((self.rect.width, mask_height))
                    mask2.rect.topleft = self.rect.topleft
                    if not level.has_suns(self.price) or self.cd_percentage < 1:
                        self.cursor = None
                        if self.selected:
                            self.selected = None
                    else:
                        self.cursor = 'hand'
                    self.background_color = (60, 50, 30) if self.selected else (48, 30, 24)
                def onplant(e: events.UserEvent):
                    if type(e.target) is planter.type:
                        self.last_planted_lvl_ticks = level.ticks
                planter.add_event_listener('plant', onplant)
                self.update = update
                scene.add_element(mask1)
                scene.add_element(mask2)

            @property
            def price(self):
                return self.planter.price

            @property
            def cd_percentage(self):
                passed_ticks = level.ticks - self.last_planted_lvl_ticks
                return min(1, passed_ticks / self.planter.cooldown_ticks)

        self.cards = tuple(Card(i, p) for i, p in (
            (media.load_image('plants/sunflower.png', CARD_IMAGE_SIZE), plants.sun_flower.planter),
            (media.load_image('plants/peashooter.png', CARD_IMAGE_SIZE), plants.pea_shooter.planter),
            (media.load_image('plants/gatlingpea.png', CARD_IMAGE_SIZE), plants.gatling_pea.planter),
            (media.load_image('plants/snowpea.png', CARD_IMAGE_SIZE), plants.snow_pea.planter),
            (media.load_image('plants/wallnut.png', CARD_IMAGE_SIZE), plants.wall_nut.planter),
            (media.load_image('plants/potatomine.png', CARD_IMAGE_SIZE), plants.potato_mine.planter),
        ))
        span1 = element.Element((8, 8))
        span2 = element.Element((8, 8))
        span1.background_color = (0, 0, 0, 0)
        span2.background_color = (0, 0, 0, 0)
        self.card_board_sun_icon = element.Element(media.load_image('entities/sun.png', (CARD_IMAGE_SIZE[0] * 0.8, CARD_IMAGE_SIZE[1] * 0.8)))
        self.card_board = element.Element(None, ROW, [
            element.Element(None, None, [
                span1,
                self.card_board_sun_icon,
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
    def victory(self) -> bool | None:
        return self.__victory.value
    
    @victory.setter
    def victory(self, value: bool | None):
        self.__victory.value = value
    
    @property
    def selected_planter(self):
        for card in self.cards:
            if card.selected:
                return card.planter
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
        selected_planter = self.selected_planter
        def grow_plant(_tile: Tile):
            def listener(e: events.ClickEvent):
                target_tile: Tile = e.target
                if _tile is target_tile and _tile.growable:
                    _tile.planter = selected_planter
                    for card in self.cards:
                        card.selected = False
            return listener
        for row in self.tiles:
            for tile in row:
                if tile.growable:
                    if selected_planter is not None:
                        tile.cursor = 'hand'
                        tile.add_event_listener(events.CLICK, grow_plant(tile))
                    else:
                        tile.cursor = None
                        tile.remove_event_listener(events.CLICK, remove_all=True)
        self.ticks += 1

from components import controller