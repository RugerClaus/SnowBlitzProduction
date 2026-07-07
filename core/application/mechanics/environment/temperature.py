class Temperature:
    def __init__(self, system,daycycle):
        self.math = system.math
        self.daycycle = daycycle
        self.temperature = 0

    def update(self):
        progress = self.daycycle.get_time_progress()

        min_temp = -10
        max_temp = 30

        heat = (self.math.sin(progress * 2 * self.math.pi - self.math.pi/2) + 1) / 2

        self.temperature = min_temp + (max_temp - min_temp) * heat

    def get_temperature(self):
        return self.temperature