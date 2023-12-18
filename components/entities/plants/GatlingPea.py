from utils.constants import *
from components.entities.plants import Shooter, Planter
from components.media import media
import utils.asynclib as asynclib

health = 350
price = 200
plant_cooldown_ticks = 5 * FPS

class GatlingPea(Shooter):
    def __init__(self):
        from components.entities.plants.PeaShooter import pea_template
        Shooter.__init__(
            self,
            media.load_image('plants/gatlingpea.png', PLANT_SIZE),
            media.load_image('plants/gatlingpea_attack.png', PLANT_SIZE),
            price,
            (0.5, 0.35),
            pea_template,
            120,
        )
        self.health = health
        self.fov = TILE_WIDTH * 10
    
    def shoot(self):
        # 改寫連發射手的發射方法
        Shooter.shoot(self)
        asynclib.set_timeout(lambda: Shooter.shoot(self), 50)

planter = Planter(GatlingPea, price, plant_cooldown_ticks)