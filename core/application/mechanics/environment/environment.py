from core.application.mechanics.environment.daycycle import DayCycle
from core.application.mechanics.environment.temperature import Temperature
from core.application.entities.sun.sun import Sun
from core.application.mechanics.environment.season import Season
class Environment:
    def __init__(self,system):
        self.system = system
        self.day_cycle = DayCycle(system)
        self.sun = Sun(system,self.day_cycle)
        self.season = Season(self.day_cycle)
        self.season.winter()
        self.temperature = Temperature(system,self.day_cycle,self.season)
        

    def update(self):
        self.day_cycle.update()
        self.sun.update()
        self.season.update_season()
        self.season.update()
        self.temperature.update()

    def draw(self):
        self.day_cycle.draw()
        self.sun.draw()