import math
from core.game.entities.entity import Entity
from core.game.entities.type import EntityType
from helper import asset

class Sun(Entity):
    def __init__(self, board_surface,day_cycle):
        self.board_surface = board_surface
        self.day_cycle = day_cycle
        self.spawn()
        super().__init__(
            self.x,
            self.y,
            board_surface,
            EntityType.SUN
        )
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def spawn(self):
        self.x = self.board_surface.get_width() + 100
        self.y = 100
        self.speed = 50
        self.amplitude = 50
        self.surface = self.board_surface.load_image(asset("title"))

        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.total_time = 0 

    def update(self):
        progress = self.day_cycle.get_time_progress()
        self.x = self.board_surface.get_width() + progress * (self.board_surface.get_width() + 200)

        self.y = 100 + self.amplitude * math.sin(math.pi * self.x / self.board_surface.get_width())

        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self):
        self.board_surface.blit(self.surface, self.rect)
