from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate, Planter
from components.media import media
from components.entities.zombies import Zombie

health = 100
price = 100
plant_cooldown_ticks = 3 * FPS

pea_template = BulletTemplate(
    media.load_image('entities/pea.png', BULLET_SIZE),
    BULLET_SPEED,
    None,
    25,
    [Zombie]
)

class PeaShooter(Shooter):
    def __init__(self):
        Shooter.__init__(
            self,
            media.load_image('plants/peashooter.png', PLANT_SIZE),
            media.load_image('plants/peashooter_attack.png', PLANT_SIZE),
            price,
            (0.5, 0.35),
            pea_template,
            120,
        )
        self.health = health
        self.fov = TILE_WIDTH * 10

planter = Planter(PeaShooter, price, plant_cooldown_ticks)