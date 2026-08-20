import random

from core.application.SnowBlitz.entities.type import EntityType
from core.application.SnowBlitz.entities.entity import Entity


class SnowFlake(Entity):

    def __init__(self, system):

        self.system = system

        self.spawn()

        super().__init__(
            self.x,
            self.y,
            system.window,
            EntityType.SNOWFLAKE,
            self.diam
        )

        self.rect = self.surface.get_rect(
            topleft=(self.x, self.y)
        )


    def spawn(self):

        self.x = random.randint(
            90,
            self.system.window.get_width() - 90
        )

        self.y = random.randint(
            -600,
            0
        )

        self.diam = random.randint(
            1,
            30
        )

        self.speed = 0

        self.surface = self.system.window.make_surface(
            self.diam,
            self.diam,
            True
        )

        if hasattr(self, "rect"):
            self.rect = self.surface.get_rect(
                topleft=(self.x, self.y)
            )


    def update(self):

        acceleration = 0.03
        max_speed = 10

        if self.speed < max_speed:
            self.speed += acceleration

        self.y += self.speed

        self.rect.topleft = (
            self.x,
            self.y
        )

        if self.y > self.system.window.get_height() + 100:
            self.spawn()


    def collected(self):

        self.spawn()


    def draw(self):

        self.surface.fill(
            (0, 0, 0, 0)
        )

        self.system.window.draw_circle(
            self.surface,
            (255, 255, 255),
            (
                self.diam / 2,
                self.diam / 2
            ),
            self.diam / 2,
            self.type
        )

        self.system.window.blit(
            self.surface,
            self.rect
        )