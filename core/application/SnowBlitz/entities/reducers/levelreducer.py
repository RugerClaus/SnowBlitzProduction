import random

from core.application.SnowBlitz.entities.entity import Entity
from core.application.SnowBlitz.entities.type import EntityType
from core.application.SnowBlitz.entities.reducers.type import LRType
from core.ui.font import FontEngine


class LevelReducer(Entity):

    def __init__(self, system, reducer_type: LRType):

        self.system = system
        self.reducer_type = reducer_type

        self.color = (128, 100, 190)
        self.diam = 50

        self.font = FontEngine(30).font

        self.spawn()

        super().__init__(
            self.x,
            self.y,
            system.window,
            EntityType.REDUCER,
            self.diam
        )

        self.rect = self.surface.get_rect(
            topleft=(self.x, self.y)
        )


    def get_reducer_number(self):
        pass


    def spawn(self):

        self.x = random.randint(
            35,
            self.system.window.get_width() - 35
        )

        self.y = random.randint(
            -200,
            0
        )

        self.speed = 0

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

        self.surface.fill(
            self.color
        )

        self.system.window.draw_circle(
            self.surface,
            (255, 255, 255),
            (
                self.diam / 2,
                self.diam / 2
            ),
            self.diam / 3,
            self.reducer_type
        )

        self.draw_reducer_number(
            self.surface
        )


    def update(self):

        acceleration = 0.05
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


    def draw_reducer_number(self, base_surface):

        text = f"{self.get_reducer_number()}"

        surface = self.font.render(
            text,
            True,
            (248, 0, 90)
        )

        rect = surface.get_rect()

        rect.center = (
            base_surface.get_rect().center
        )

        base_surface.blit(
            surface,
            rect
        )


    def draw(self):

        self.system.window.blit(
            self.surface,
            self.rect
        )