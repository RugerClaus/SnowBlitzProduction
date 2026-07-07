import math

class DayCycle:
    def __init__(self, system):
        self.system = system
        self.day_length = 100000
        self.start_phase = 0
        self.current_time = 0
        self.last_update_time = system.time.get_current_time()
        self.brightness = None

    def update(self):
        current_time = self.system.time.get_current_time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time

        self.current_time += delta_time
        if self.current_time > self.day_length:
            self.current_time -= self.day_length

    def get_time_progress(self):
        progress = (self.current_time / self.day_length + self.start_phase) % 1.0
        return progress
    
    def get_day_night_color(self):
        progress = self.get_time_progress()

        night = (20, 30, 80)
        day = (135, 206, 235)

        self.brightness = (math.sin(progress * 2 * math.pi - math.pi/2) + 1) / 2

        r = int(night[0] + (day[0] - night[0]) * self.brightness)
        g = int(night[1] + (day[1] - night[1]) * self.brightness)
        b = int(night[2] + (day[2] - night[2]) * self.brightness)

        self.system.window.fill((r, g, b))

    def draw(self):
        self.get_day_night_color()

    def get_brightness(self):
        return int(self.brightness * 100) if self.brightness is not None else "brightness not set"
    
    def get_daytime(self):
        return int(self.current_time / 1000)
    
    def reset(self):
        self.current_time = 0
        self.last_update_time = self.system.time.get_current_time()
        self.brightness = None