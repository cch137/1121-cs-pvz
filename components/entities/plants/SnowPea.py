from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie
from components.entities import SlowDownEffect

pea_ice_template = BulletTemplate(
    media.load_image('entities/icepea.png', BULLET_SIZE),
    BULLET_SPEED,
    None,
    10,
    [Zombie],
    [SlowDownEffect('SnowPea', 180, 0.5)]
)

class SnowPea(Shooter):
    def __init__(self):
        Shooter.__init__(
            self,
            media.load_image('plants/snowpea.png', PLANT_SIZE),
            media.load_image('plants/snowpea_attack.png', PLANT_SIZE),
            175,
            (0.5, 0.4),
            pea_ice_template,
            150,
        )
        self.health = 75
        self.fov = TILE_WIDTH * 10