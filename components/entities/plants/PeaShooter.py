from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie

pea_template = BulletTemplate(
                media.load_image("") , 
                (0.5, 0.5),
                BULLET_SPEED,
                None,
                25,
                [Zombie]
            )

class PeaShooter(Shooter):
    def __init__(self):
        Shooter.__init__(
            self,
            media.load_image("#原圖"),
            100,
            (0.5, 0.5),
            pea_template,
            60,
        )
        self.health = 100
        self.fov = TILE_WIDTH * 10
