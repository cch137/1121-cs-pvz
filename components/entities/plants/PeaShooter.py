from utils.constants import *
from components.entities.plants import Shooter, BulletTemplate
from components.media import media
from components.entities.zombies import Zombie

pea_template = BulletTemplate(
    media.load_image('demo/PeaNormal_0.png', BULLET_SIZE),
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
            100,
            (0.5, 0.5),
            pea_template,
            120,
        )
        self.health = 100
        self.fov = TILE_WIDTH * 10
