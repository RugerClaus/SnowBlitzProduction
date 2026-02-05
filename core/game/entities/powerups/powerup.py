import random
from core.game.entities.entity import Entity
from core.game.entities.type import EntityType
from core.game.entities.powerups.type import PowerUpType

class PowerUp(Entity):
    def __init__(self,board_surface, diam, power_type: PowerUpType):
        self.board_surface = board_surface
        self.power_type = power_type
        self.diam = diam
        self.spawn()
        super().__init__(self.x, self.y, board_surface, EntityType.POWERUP, self.diam)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def get_powerup_color(self):   
        if self.power_type == PowerUpType.GROW:
            return (255, 0, 0)

    def spawn(self):
        self.x = random.randint(35, self.board_surface.get_width()-35)
        self.y = random.randint(-600, 0)
        self.diam = self.diam
        self.color = self.get_powerup_color()
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
        self.surface.fill((0,0,0,0))
        self.board_surface.draw_circle(self.surface, self.color, (self.diam // 2, self.diam // 2), float(self.diam // 2),self.type)
        self.board_surface.blit(self.surface, self.rect)