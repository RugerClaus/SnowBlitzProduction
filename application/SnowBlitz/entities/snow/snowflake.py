from application.SnowBlitz.entities.type import EntityType
from application.SnowBlitz.entities.entity import Entity
from core.engine.textureatlas import TextureAtlas


class SnowFlake(Entity):

    def __init__(self, system, camera=None):
        self.system = system
        self.camera = camera

        self.texture_atlas = TextureAtlas(
            system,
            "snowflakes",
            "snowflakes",
            3,
            4
        )

        self.surface = None

        self.world_x = 0.0
        self.world_y = 0.0

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.camera_follow_x = 1.0
        self.camera_follow_y = 1.0

        self.wrap_x = False
        self.wrap_y = False

        self.diam = 1
        self.speed = 0.0

        self.acceleration = 100.0
        self.max_speed = 600.0

        self.drift_x = 0.0

        self.spawn_margin_x = 0.1
        self.spawn_margin_y = 0.5

        self.rotation = 0.0
        self.rotation_speed = 0.0

        self.base_surface = None

        self.spawn()

        super().__init__(
            0,
            0,
            system.window,
            EntityType.SNOWFLAKE,
            self.diam
        )

        self.rect = self.surface.get_rect()

        self.update_screen_position()

    def set_camera(self, camera):
        self.camera = camera
        self.update_screen_position()

    def spawn(self):
        self.diam = self.system.random.randint(1, 30)
        self.speed = 0.0
        self.drift_x = self.system.random.uniform(-0.02, 0.02)
        self.rotation = self.system.random.uniform(0.0, 360.0)
        self.rotation_speed = self.system.random.uniform(-180.0, 180.0)

        source = self.texture_atlas.get(
            self.system.random.randint(
                0,
                len(self.texture_atlas) - 1
            )
        )

        self.base_surface = self.system.window.transform_scale(
            source,
            self.diam,
            self.diam
        )

        self.surface = self.system.window.transform_rotate(
            self.base_surface,
            self.rotation
        )

        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        self.world_x = camera_x + self.system.random.uniform(
            -self.spawn_margin_x,
            1.0 + self.spawn_margin_x
        )

        self.world_y = camera_y - self.system.random.uniform(
            0.0,
            self.spawn_margin_y
        )

        if hasattr(self, "rect"):
            self.update_screen_position()

    def get_screen_position(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        screen_x = (
            self.world_x - camera_x * self.camera_follow_x
        ) * ww

        screen_y = (
            self.world_y - camera_y * self.camera_follow_y
        ) * wh

        return round(screen_x), round(screen_y)

    def update_screen_position(self):
        screen_x, screen_y = self.get_screen_position()
        self.rect.topleft = (screen_x, screen_y)

    def update(self):
        dt = self.system.time.delta_time()

        if self.speed < self.max_speed:
            self.speed += self.acceleration * dt
            self.speed = min(self.speed, self.max_speed)

        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        if wh <= 0:
            return

        self.world_y += (self.speed / wh) * dt
        self.world_x += self.drift_x * dt
        self.world_x += self.velocity_x * dt
        self.world_y += self.velocity_y * dt

        if self.wrap_x:
            self.world_x %= 1.0

        if self.wrap_y:
            self.world_y %= 1.0

        self.rotation += self.rotation_speed * dt
        self.rotation_speed *= 0.995

        self.surface = self.system.window.transform_rotate(
            self.base_surface,
            self.rotation
        )

        self.update_screen_position()

        if self.rect.top > wh * 0.9:
            self.spawn()

    def collected(self):
        self.spawn()

    def draw(self):
        self.system.window.blit(
            self.surface,
            self.rect
        )