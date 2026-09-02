from application.SnowBlitz.entities.entity import Entity
from application.SnowBlitz.entities.type import EntityType
from application.SnowBlitz.entities.powerups.type import PowerUpType
from core.ui.widgets.image import Image


class PowerUp(Entity):

    def __init__(self, system, diam, power_type: PowerUpType, image_path=None, camera=None):
        self.system = system
        self.camera = camera
        self.power_type = power_type
        self.diam = diam
        self.image_path = image_path
        self.image = None

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

        super().__init__(0, 0, system.window, EntityType.POWERUP, self.diam)

        self.spawn()

        self.rect = self.surface.get_rect(topleft=(0, 0)) if self.surface else self.image.rect
        self.update_screen_position()

    def set_camera(self, camera):
        self.camera = camera
        self.update_screen_position()

    def spawn(self):
        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        self.world_x = camera_x + self.system.random.uniform(0.05, 0.95)
        self.world_y = camera_y - self.system.random.uniform(0.05, 0.15)

        self.speed = 0.0
        self.color = self.get_powerup_color()

        if self.image_path:
            self.image = Image(self.system, f"powerup_{self.power_type}", self.image_path)
            self.surface = self.image.surf
        else:
            self.image = None
            self.surface = self.system.window.make_surface(self.diam, self.diam, True)
            self.render()

        if hasattr(self, "rect"):
            self.rect = self.surface.get_rect()
            self.update_screen_position()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        self.system.window.draw_circle(self.surface, self.color, (self.diam / 2, self.diam / 2), self.diam / 2, object=self.power_type)

    def get_screen_position(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        screen_x = (self.world_x - camera_x * self.camera_follow_x) * ww
        screen_y = (self.world_y - camera_y * self.camera_follow_y) * wh

        return round(screen_x), round(screen_y)

    def update_screen_position(self):
        x, y = self.get_screen_position()

        if self.image:
            self.image.rect = self.image.surf.get_rect(topleft=(x, y))
            self.rect = self.image.rect
        else:
            self.rect.topleft = (x, y)

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

        if self.rect.top > wh + 100:
            self.spawn()

    def collected(self):
        self.spawn()

    def draw(self):
        if self.image:
            self.system.window.blit(self.image.surf, self.image.rect)
        else:
            self.system.window.blit(self.surface, self.rect)