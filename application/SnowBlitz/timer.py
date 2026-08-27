class GameTimer:
    def __init__(self, system):
        self.system = system
        self.elapsed_ms = 0
        self.last_time = self.system.time.get_current_time()

    def update(self):
        now = self.system.time.get_current_time()
        self.elapsed_ms += now - self.last_time
        self.last_time = now

    def reset(self):
        self.elapsed_ms = 0
        self.last_time = self.system.time.get_current_time()

    def get_milliseconds(self):
        return self.elapsed_ms

    def get_seconds(self):
        return self.elapsed_ms // 1000

    def get_minutes(self):
        return self.elapsed_ms // 60000

    def get_display_time(self):
        seconds = (self.elapsed_ms // 1000) % 60
        minutes = self.elapsed_ms // 60000
        return f"{minutes:02}:{seconds:02}"

    def resume(self):
        self.last_time = self.system.time.get_current_time()