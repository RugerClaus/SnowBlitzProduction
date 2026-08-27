from application.SnowBlitz.entities.powerups.powerup import PowerUp
from application.SnowBlitz.entities.powerups.type import PowerUpType


class SpeedBoost(PowerUp):

    def __init__(self, system, camera=None):
        diam = 64
        image_path = "clock"

        super().__init__(system, diam, PowerUpType.SPEED_BOOST, image_path=image_path, camera=camera)

    def get_powerup_color(self):
        return (0, 255, 0)