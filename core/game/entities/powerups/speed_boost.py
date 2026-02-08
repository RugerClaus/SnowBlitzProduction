from core.game.entities.powerups.powerup import PowerUp
from core.game.entities.powerups.type import PowerUpType

class SpeedBoost(PowerUp):
    def __init__(self, board_surface):
        diam = 64
        image_path = "clock"
        super().__init__(board_surface, diam, PowerUpType.SPEED_BOOST,image_path)

    def get_powerup_color(self):
        return (0, 255, 0)
