# ah finally time to start fucking with sine functions
# i knew this day would come, just i wanted to implement a day night cycle for more interesting gameplay

import math

class DayCycle:
    def __init__(self, board_surface, day_length=100, start_phase=0):
        self.board_surface = board_surface
        self.day_length = day_length
        self.start_phase = start_phase
        self.time_accumulator = 0

    def update(self):
        self.time_accumulator += self.board_surface.get_delta_time()

    def get_time_progress(self):
        return (self.time_accumulator / self.day_length) % 1
    
    def get_elapsed_seconds(self):
        return self.time_accumulator

    def get_sine_value(self):
        progress = self.get_time_progress()
        angle = 2 * math.pi * progress + self.start_phase
        return (math.sin(angle) + 1) / 2

    def get_sky_color(self, day_color=(135, 206, 235), night_color=(25, 25, 112)):
        pulse = self.get_sine_value()
        return tuple(
            int(night_color[i] + (day_color[i] - night_color[i]) * pulse)
            for i in range(3)
        )
