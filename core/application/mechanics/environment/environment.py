from core.application.mechanics.environment.daycycle import DayCycle
from core.application.mechanics.environment.temperature import Temperature
from core.application.entities.sun.sun import Sun
class Environment:
    def __init__(self,system):
        self.system = system
        self.day_cycle = DayCycle(system.window)
        self.sun = Sun(system,self.day_cycle)
        self.temperature = Temperature(system,self.day_cycle)

    def update(self):
        self.day_cycle.update()
        self.temperature.update()
        self.sun.update()

    def draw(self):
        self.day_cycle.draw()
        self.sun.draw()