from utils.constants import *
from components.entities.plants import Shooter
from components.media import media
import utils.asynclib as asynclib

class GatlingPea(Shooter):
    def __init__(self):
        from components.entities.plants.PeaShooter import pea_template
        Shooter.__init__(
            self,
            media.load_image('demo/RepeaterPea_0.png', PLANT_SIZE),
            200,
            (0.5, 0.5),
            pea_template,
            120,
        )
        self.health = 100
        self.fov = TILE_WIDTH * 10
    
    def shoot(self):
        # 改寫連發射手的發射方法
        Shooter.shoot(self)
        asynclib.set_timeout(lambda: Shooter.shoot(self), 50)
