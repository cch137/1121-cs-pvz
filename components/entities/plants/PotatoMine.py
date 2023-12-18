from utils.constants import *
from components.entities import Character
from components.entities.plants import Plant, all_plants, all_zombies, Planter
from components.media import media
import utils.asynclib as asynclib

health = 1000
price = 25
plant_cooldown_ticks = 5 * FPS

class Explosion(Character):
    def __init__(self):
        Character.__init__(self, media.load_image('plants/potatomine.png', PLANT_SIZE), all_plants, all_zombies)
        asynclib.set_timeout(lambda: self.bomb(), 500)
        self.z_index = 999
        self.health  = 999999
        self.visible = False

    def bomb(self):
        self.image = media.load_image('plants/potatomine_boom.png', (PLANT_SIZE[0] * 2, PLANT_SIZE[1] * 2))
        for enemy in self.enemies_in_radius(TILE_WIDTH):
            try: enemy.kill()
            except: pass
        asynclib.set_timeout(lambda: self.kill(), 1500)

class PotatoMine(Plant):
    def __init__(self):
        Plant.__init__(self, media.load_image('plants/potatomine.png', PLANT_SIZE), price)
        self.health = health
        self.fov = 0.5 * TILE_WIDTH
        self.visible = False

    def update(self):
        if self.has_seen_enemy(True, True):
            expl = Explosion()
            self.scene.add_element(expl)
            expl.rect.center = self.rect.center
            self.kill()

planter = Planter(PotatoMine, price, plant_cooldown_ticks)