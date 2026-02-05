import random
from helper import asset
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity


class MultiplierUpgrade(Entity):
    def __init__(self, board_surface):
        self.board_surface = board_surface
        self.x = random.randint(90, board_surface.get_width() - 90)
        self.y = random.randint(-600, 0)
        self.speed = 0

        self.surface = board_surface.load_image(asset("multiplierupgrade"))

        super().__init__(self.x,self.y,board_surface,EntityType.MULTIPLIER_UPGRADE)

        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.active = True

    def update(self):
        if not self.active:
            return

        acceleration = 0.03
        self.speed = min(self.speed + acceleration, 10)
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

        if self.y > self.board_surface.get_height():
            self.active = False

    def collected(self):
        self.active = False

    def draw(self):
        if self.active:
            self.board_surface.blit(self.surface, self.rect)
