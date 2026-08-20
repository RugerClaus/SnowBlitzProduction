import random

from helper import asset
from systemlogging import log_event

from core.application.SnowBlitz.entities.entity import Entity
from core.application.SnowBlitz.entities.type import EntityType
from core.application.SnowBlitz.entities.powerups.type import PowerUpType


class PowerUp(Entity):

    def __init__(self, system, diam, power_type: PowerUpType, image_path=None):

        self.system = system

        self.power_type = power_type
        self.diam = diam
        self.image_path = image_path

        self.spawn()

        super().__init__(
            self.x,
            self.y,
            system.window,
            EntityType.POWERUP,
            self.diam
        )

        self.rect = self.surface.get_rect(
            topleft=(self.x, self.y)
        )


    def spawn(self):

        self.x = random.randint(
            35,
            self.system.window.get_width() - 35
        )

        self.y = random.randint(
            -600,
            0
        )

        self.color = self.get_powerup_color()

        self.speed = 0


        if self.image_path:

            self.surface = self.system.window.load_image(
                asset(self.image_path)
            )

            log_event(
                "successfully loaded image"
            )

        else:

            self.surface = self.system.window.make_surface(
                self.diam,
                self.diam,
                True
            )

            self.render()


        if hasattr(self, "rect"):

            self.rect = self.surface.get_rect(
                topleft=(self.x, self.y)
            )


    def render(self):

        self.surface.fill(
            (0, 0, 0, 0)
        )

        self.system.window.draw_circle(
            self.surface,
            self.color,
            (
                self.diam / 2,
                self.diam / 2
            ),
            self.diam / 2,
            self.power_type
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

        self.system.window.blit(
            self.surface,
            self.rect
        )