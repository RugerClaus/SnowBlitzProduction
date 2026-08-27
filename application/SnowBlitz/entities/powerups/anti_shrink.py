from application.SnowBlitz.entities.powerups.powerup import PowerUp
from application.SnowBlitz.entities.powerups.type import PowerUpType

class AntiShrink(PowerUp):
    def __init__(self, board_surface,camera=None):
        diam = 10
        super().__init__(board_surface, diam, PowerUpType.ANTI_SHRINK,camera=camera)

    def get_powerup_color(self):
        return (0, 255, 0)