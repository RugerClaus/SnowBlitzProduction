import random,pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity

class Rock(Entity):
    def __init__(self, board_surface):
        self.board_surface = board_surface
        colors = [
            (112, 128, 144),  # Slate Gray
            (169, 169, 169),  # Dark Gray
            (105, 105, 105),  # Dim Gray
            (128, 128, 128),  # Classic Gray
            (192, 192, 192),  # Light Gray
            (101, 67, 33),    # Brown (earthy rock)
            (87, 85, 83),     # Granite
            (70, 70, 70),     # Charcoal
            (115, 105, 92),   # Weathered limestone
            (143, 129, 118),  # Sandstone
            (88, 80, 68),     # Basalt
            (108, 122, 137),  # Cool-toned shale
            (135, 115, 90),   # Desert rock
        ]
        self.spawn()
        self.surface.fill(random.choice(colors))
        super().__init__(self.x, self.y, board_surface, EntityType.ROCK)

    def spawn(self):
        self.x = random.randint(0, self.board_surface.get_width())
        self.y = random.randint(-600, -200)
        self.speed = 0
        self.width = random.randint(30,50)
        self.height = random.randint(30,50)
        self.surface = self.board_surface.make_surface(self.width,self.height)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
 
        

    def update(self):
        acceleration = 0.1
        self.speed += acceleration
        self.y += self.speed
        if self.speed >= 10:
            acceleration = 0
        self.rect.topleft = (self.x, self.y)
        if self.y > self.board_surface.get_height() - 100:
            self.spawn()

    def draw(self):
        self.board_surface.blit(self.surface, self.rect)