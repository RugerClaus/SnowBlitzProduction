from core.application.entities.entity import Entity
from core.application.entities.type import EntityType

class Sun(Entity):
    def __init__(self,system,daycycle):
        self.system = system
        self.daycycle = daycycle
        self.type = EntityType.SUN
        self.surface = self.system.window.make_surface(200,200,True)
        self.rect = self.surface.get_rect(topright=(self.system.window.get_width() + 300 , 0))
        self.color = (255,255,0)
        self.horizon = self.system.window.get_height() // 10 + self.rect.height
        self.arc_height = self.system.window.get_height() * 0.001
        self.size = float(self.rect.width // 2)
        
    def update(self):

        math = self.system.math

        progress = self.daycycle.get_sun_progress()

        if progress is None:
            self.rect.centerx = -self.rect.width
            self.rect.centery = self.horizon + self.rect.height
            self.position = self.rect.center
            return


        sw = self.system.window.get_width()

        travel_distance = (
            sw
            +
            self.rect.width
            +
            200
        )

        self.rect.centerx = (
            sw
            +
            100
            -
            travel_distance
            *
            progress
        )


        self.rect.centery = (
            self.horizon
            -
            self.arc_height
            -
            self.rect.height
            *
            math.sin(
                math.pi
                *
                progress
            )
        )

        self.position = self.rect.center


    def draw(self):
        self.surface.fill(
            (0, 0, 0, 0)
        )
        self.system.window.draw_circle(
            self.surface,
            self.color,
            (
                self.size,
                self.size
            ),
            self.size,
            self.type
        )
        self.system.window.blit(self.surface,self.rect.topleft)