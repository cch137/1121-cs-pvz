from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie
from components.entities.__init__ import SlowDownEffect

    
class SnowPea(Shooter):
    def __init__(self):
        Shooter.__init__(
            self,
            media.load_image('demo/SnowPea_0.png', PLANT_SIZE),
            175,
            (0.5, 0.5),
            BulletTemplate(
                media.load_image('demo/PeaIce_0.png', BULLET_SIZE) , 
                BULLET_SPEED,
                None,
                15,
                [Zombie]
                [SlowDownEffect('SnowPea', 120, 0.3)]
            ),
            60,
        )
        self.health = 75
        self.fov = TILE_WIDTH * 10