from utils.constants import *
from components.entities import Character
from components.entities.plants import Plant, all_plants, all_zombies
from components.media import media
from components.entities.zombies import Zombie
import utils.asynclib as asynclib

class Explosion(Character):
    def __init__(self):
        Character.__init__(self, media.load_image('demo/PotatoMine_0.png', PLANT_SIZE), all_plants, all_zombies)
        asynclib.set_timeout(lambda: self.bomb(), 500)
        self.z_index = 999
        self.health  = 999999
        self.targets = set()
    
    def update(self):
        for enemy in self.enemies_in_radius(TILE_WIDTH):
            self.targets.add(enemy)

    def bomb(self):
        self.image = media.load_image('demo/PotatoMineExplode_0.png', (PLANT_SIZE[0] * 2, PLANT_SIZE[1] * 2 * 0.7))
        for enemy in self.targets:
            try: enemy.kill()
            except: pass
        asynclib.set_timeout(lambda: self.kill(), 3000)

class PotatoMine(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('demo/PotatoMine_0.png', PLANT_SIZE), 25)
        self.health = 1000
        self.fov = 0.25 * TILE_WIDTH

    def auto_update(self):
        if self.has_seen_enemy(True, True):
            expl = Explosion()
            self.scene.add_element(expl)
            expl.rect.center = self.rect.center
            self.kill()
