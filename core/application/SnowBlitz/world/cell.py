from core.util.colors import *


class Cell:
    def __init__(self, system, color, size=(0.01, 0.01), position=(0, 0)):
        self.system = system

        self.x, self.y = position
        self.width, self.height = size

        self.color = color

        self.surface = None
        self.scale()

    def scale(self, width=None, height=None):
        if width is None or height is None:
            ww = self.system.window.get_width()
            wh = self.system.window.get_height()

            width = round(self.width * ww)
            height = round(self.height * wh)

        self.surface = self.system.window.make_surface(
            width,
            height,
            True
        )

        if self.color:
            self.surface.fill(self.color)
            if self.color:
                self.surface.fill(self.color)

    def get_rect(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        pixel_x = round(self.x * ww)
        pixel_y = round(self.y * wh)

        return self.surface.get_rect(
            center=(pixel_x, pixel_y)
        )

    def draw_debug_border(self, color=None, width=None):
        if not color:
            color = white

        if not width:
            width = 1

        self.system.window.draw_rect(
            self.surface,
            color,
            self.surface.get_rect(),
            width=width
        )

    def update(self):
        pass