import pygame
from typing import Dict, List, Optional
from core.game.entities.type import EntityType

# below is a mach up for entity pools.

# LIMITS: Dict[EntityType, int] = {
#     EntityType.PLAYER: 1,
#     EntityType.POWERUP: 5,
#     EntityType.SNOWFLAKE: 80,
#     EntityType.ROCK: 20,
#     EntityType.REDUCER: 10,
# }

class Entity:
    def __init__(self, x, y, board_surface, type: EntityType, size=None):
        self.x = x
        self.y = y
        self.type = type
        self.size = size
        self.board_surface = board_surface

    def update(self):
        pass

    def draw(self):
        pass