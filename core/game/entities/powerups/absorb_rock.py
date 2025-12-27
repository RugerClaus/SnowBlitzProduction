from core.game.entities.powerups.powerup import PowerUp
from core.game.entities.powerups.type import PowerUpType

class AbsorbRock(PowerUp):
    def __init__(self, board_surface):
        diam = 15
        super().__init__(board_surface, diam, PowerUpType.ABSORB_ROCK)