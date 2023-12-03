from utils.constants import *
from components.entities import Character
from components.entities.plants import Plant, all_plants, all_zombies
from components.media import media
from components.entities.zombies import Zombie
import utils.asynclib as asynclib

class Explosion(Character):
    def __init__(self):
        Character.__init__(self, media.load_image('#原圖', (50, 50)), all_plants, all_zombies)
        asynclib.set_timeout(lambda: self.bomb(), 500)

    def bomb(self):
        for enemy in self.enemies_in_radius(TILE_WIDTH):
            enemy.kill()
        self.image = media.load_image('#爆炸', (50, 50))
        asynclib.set_timeout(lambda: self.kill(), 1000)

class PotatoMine(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('#原圖', (50, 50)), 25)
        self.health = 1000
        self.fov = 0.25 * TILE_WIDTH

    def auto_update(self):
        if self.has_seen_enemy(True, True):
            self.kill()
            self.tile.append_child(Explosion())
