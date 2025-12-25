import random,pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity

class SnowFlake(Entity):
    def __init__(self, board_surface):
        self.board_surface = board_surface
        # self.spawn()
        self.x = 500
        self.y = 100
        self.size = random.randint(1,30)
        
        self.speed = 0
        self.surface = self.board_surface.make_surface(self.size,self.size)
        self.rect = self.surface.get_rect()
        super().__init__(self.x, self.y, board_surface, EntityType.SNOWFLAKE, self.size)
        

    def spawn(self):
        self.size = random.randint(1,30)
        
        self.speed = 0.01
        self.surface = self.board_surface.make_surface(self.size,self.size)
        self.rect = self.surface.get_rect()

    def update(self):
        # acceleration = 0.03
        # self.speed += acceleration
        # self.y += self.speed
        # if self.speed >= 10:
        #     acceleration = 0
        # self.rect.topleft = (self.x, self.y)
        # if self.y > self.board_surface.get_height() - 100:
        #     self.speed
        pass

    def draw(self):
        pygame.draw.circle(self.surface, (255, 255, 255), (self.size // 2, self.size // 2), self.size // 2)
        self.board_surface.blit(self.surface, self.rect)