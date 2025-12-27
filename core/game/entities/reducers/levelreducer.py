import random, pygame
from core.game.entities.entity import Entity
from core.game.entities.type import EntityType
from core.game.entities.reducers.type import LRType
from core.ui.font import FontEngine

class LevelReducer(Entity):
    def __init__(self,board_surface, reducer_type: LRType):
        self.board_surface = board_surface
        self.reducer_type = reducer_type
        self.color = (128,100,190)
        self.diam = 50
        self.font = FontEngine(30).font
        self.spawn()
        super().__init__(self.x, self.y, board_surface, EntityType.REDUCER, self.diam)

    def get_reducer_number(self):
        pass

    def spawn(self):
        self.x = random.randint(35, self.board_surface.get_width()-35)
        self.y = random.randint(-200, 0)
        self.diam = self.diam
        self.speed = 0
        self.surface = self.board_surface.make_surface(self.diam,self.diam)
        self.rect = self.surface.get_rect()

    def update(self):
        acceleration = 0.05
        self.speed += acceleration
        self.y += self.speed
        if self.speed >= 10:
            acceleration = 0
        self.rect.topleft = (self.x, self.y)
        if self.y > self.board_surface.get_height() - 100:
            self.spawn()

    def collected(self):
        self.spawn()            

    def draw_reducer_number(self,base_surface):
        text = f"{self.get_reducer_number()}"
        surface = self.font.render(text,True,(248,0,90))
        rect = surface.get_rect()
        rect.center = base_surface.get_rect().center
        base_surface.blit(surface,rect)

    def draw(self):
        self.surface.fill(self.color)
        pygame.draw.circle(self.surface, (255,255,255), (self.diam // 2, self.diam // 2), self.diam // 3)
        self.draw_reducer_number(self.surface)
        self.board_surface.blit(self.surface, self.rect)