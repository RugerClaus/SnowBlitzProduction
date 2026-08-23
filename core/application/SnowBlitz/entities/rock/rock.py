from core.application.SnowBlitz.entities.type import EntityType
from core.application.SnowBlitz.entities.entity import Entity


class Rock(Entity):

    def __init__(self, system, camera=None):
        self.system = system
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
        self.width = 40
        self.height = 40

        super().__init__(0, 0, system.window, EntityType.ROCK)

        self.spawn()

        self.rect = self.surface.get_rect(topleft=(0, 0))
        self.update_screen_position()

    def spawn(self):
        camera_x = self.camera.x if self.camera is not None else 0.0
        camera_y = self.camera.y if self.camera is not None else 0.0

        self.world_x = camera_x + self.system.random.uniform(0.1, 0.9)
        self.world_y = camera_y - self.system.random.uniform(0.05, 0.15)
        self.speed = 0.0

        self.width = self.system.random.randint(30, 50)
        self.height = self.system.random.randint(30, 50)

        self.surface = self.system.window.make_surface(self.width, self.height, True)

        colors = [
            (112, 128, 144),
            (169, 169, 169),
            (105, 105, 105),
            (128, 128, 128),
            (192, 192, 192),
            (101, 67, 33),
            (87, 85, 83),
            (70, 70, 70),
            (115, 105, 92),
            (143, 129, 118),
            (88, 80, 68),
            (108, 122, 137),
            (135, 115, 90)
        ]

        self.surface.fill(self.system.random.choice(colors))

        if hasattr(self, "rect"):
            self.rect = self.surface.get_rect()
            self.update_screen_position()

    def set_camera(self, camera):
        self.camera = camera
        self.update_screen_position()

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

    def draw(self):
        self.system.window.blit(self.surface, self.rect)