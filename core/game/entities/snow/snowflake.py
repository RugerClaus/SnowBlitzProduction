import random
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity

class SnowFlake(Entity):
    def __init__(self, board_surface):
        self.board_surface = board_surface
        self.spawn()
        super().__init__(self.x, self.y, board_surface, EntityType.SNOWFLAKE, self.diam)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        

    def spawn(self):
        self.x = random.randint(90, self.board_surface.get_width()-90)
        self.y = random.randint(-600, 0)
        self.diam = random.randint(1,30)
        
        self.speed = 0
        self.surface = self.board_surface.make_surface(self.diam,self.diam,True)

    def update(self):
        acceleration = 0.03
        self.speed += acceleration
        self.y += self.speed
        if self.speed >= 10:
            acceleration = 0
        self.rect.topleft = (self.x, self.y)
        if self.y > self.board_surface.get_height() + 100:
            self.spawn()

    def collected(self):
        self.spawn()            

    def draw(self):
        self.board_surface.draw_circle(self.surface, (255, 255, 255), (self.diam // 2, self.diam // 2), float(self.diam // 2),self.type)
        self.board_surface.blit(self.surface, self.rect)