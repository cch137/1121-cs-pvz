from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate, Planter
from components.media import media
from components.entities.zombies import Zombie
from components.entities import SlowDownEffect

health = 250
price = 175
plant_cooldown_ticks = 4 * FPS

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
            price,
            (0.5, 0.35),
            pea_ice_template,
            150,
        )
        self.health = health
        self.fov = TILE_WIDTH * 10

planter = Planter(SnowPea, price, plant_cooldown_ticks)