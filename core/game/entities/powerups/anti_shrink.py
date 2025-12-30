from core.game.entities.powerups.powerup import PowerUp
from core.game.entities.powerups.type import PowerUpType

class AntiShrink(PowerUp):
    def __init__(self, board_surface):
        diam = 10
        super().__init__(board_surface, diam, PowerUpType.ANTI_SHRINK)

    def get_powerup_color(self):
        return (0, 255, 0)