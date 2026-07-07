from core.application.entities.entity import Entity
from core.application.entities.type import EntityType

class Sun(Entity):
    def __init__(self,system,daycycle):
        self.system = system
        self.daycycle = daycycle
        self.type = EntityType.SUN
        self.surface = self.system.window.make_surface(200,200,False)
        self.rect = self.surface.get_rect(topright=(self.system.window.get_width() + 300 , 0))
        self.surface.fill((255,255,0))
        self.horizon = self.system.window.get_height() // 10 + self.rect.height
        self.arc_height = 50
        

    def update(self):
        math = self.system.math
        sw = self.system.window.get_width()
        self.rect.centerx = ((sw+150) - (sw+200) * self.daycycle.get_time_progress())
        self.rect.centery = self.horizon - self.rect.height * math.sin(math.pi * self.daycycle.get_time_progress())
        self.position = self.rect.center


    def draw(self):
        self.system.window.blit(self.surface,self.rect)