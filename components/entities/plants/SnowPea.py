from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie
from components.entities.__init__ import SlowDownEffect

    
class SnowPea(Shooter):
    def __init__(self):
        Shooter.__init__(
            self,
            media.load_image("#冰豌豆射手原圖"),
            175,
            (0.5, 0.5),
            BulletTemplate(
                media.load_image("#冰豌豆子彈") , 
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