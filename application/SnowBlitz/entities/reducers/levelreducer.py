from application.SnowBlitz.entities.entity import Entity
from application.SnowBlitz.entities.type import EntityType
from application.SnowBlitz.entities.reducers.type import LRType
from core.ui.font import FontEngine


class LevelReducer(Entity):

    def __init__(self, system, reducer_type: LRType, camera=None):
        self.system = system
        self.reducer_type = reducer_type
        self.camera = camera

        self.world_x = 0.0
        self.world_y = 0.0

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.camera_follow_x = 1.0
        self.camera_follow_y = 1.0

        self.wrap_x = False
        self.wrap_y = False

        self.speed = 0.0
        self.acceleration = 300.0
        self.max_speed = 600.0

        self.color = (128, 100, 190)
        self.diam = 50

        self.font = FontEngine(30).font

        super().__init__(0, 0, system.window, EntityType.REDUCER, self.diam)

        self.spawn()

        self.rect = self.surface.get_rect(topleft=(0, 0))
        self.update_screen_position()

    def get_reducer_number(self):
        pass

    def set_camera(self, camera):
        self.camera = camera
        self.update_screen_position()

    def spawn(self):
        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        self.world_x = camera_x + self.system.random.uniform(0.1, 0.9)
        self.world_y = camera_y - self.system.random.uniform(0.05, 0.15)

        self.speed = 0.0

        self.surface = self.system.window.make_surface(self.diam, self.diam, True)

        self.render()

        if hasattr(self, "rect"):
            self.rect = self.surface.get_rect()
            self.update_screen_position()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        self.surface.fill(self.color)

        self.system.window.draw_circle(
            self.surface,
            (255, 255, 255),
            (self.diam / 2, self.diam / 2),
            self.diam / 3,
            self.reducer_type
        )

        self.draw_reducer_number(self.surface)

    def get_screen_position(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        screen_x = (self.world_x - camera_x * self.camera_follow_x) * ww
        screen_y = (self.world_y - camera_y * self.camera_follow_y) * wh

        return round(screen_x), round(screen_y)

    def update_screen_position(self):
        self.rect.topleft = self.get_screen_position()

    def update(self):
        dt = self.system.time.delta_time()

        if self.speed < self.max_speed:
            self.speed = min(self.speed + self.acceleration * dt, self.max_speed)

        wh = self.system.window.get_height()

        if wh <= 0:
            return

        self.world_y += (self.speed / wh) * dt
        self.world_x += self.velocity_x * dt
        self.world_y += self.velocity_y * dt

        if self.wrap_x:
            self.world_x %= 1.0

        if self.wrap_y:
            self.world_y %= 1.0

        self.update_screen_position()

        if self.rect.top > self.system.window.get_height() + 100:
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
        rect.center = base_surface.get_rect().center

        base_surface.blit(surface, rect)

    def draw(self):
        self.system.window.blit(self.surface, self.rect)