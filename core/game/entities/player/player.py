import pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity

class Player(Entity):
    def __init__(self,surface):
        self.base_size = 10
        x = surface.get_width() // 2
        y = surface.get_height() - surface.get_height() // 8
        type = EntityType.PLAYER
        size = self.base_size
        super().__init__(x, y, type, size)