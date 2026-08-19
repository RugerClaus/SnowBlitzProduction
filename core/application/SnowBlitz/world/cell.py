from core.util.colors import *

class Cell:
    def __init__(self, system, color, size=(0.01, 0.01), position=(0, 0)):
        self.system = system
        self.x, self.y = position
        self.width, self.height = size
        self.color = color

        self.scale()

    def scale(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        true_position = (self.x * ww, self.y * wh)
        true_size = (self.width * ww, self.height * wh)

        self.surface = self.system.window.make_surface(*true_size, True)

        if self.color:
            self.surface.fill(self.color)

        self.rect = self.surface.get_rect(center=true_position)

    def draw_debug_border(self,color=None,width=None):
        rect = self.surface.get_rect()
        if not color:
            color = white
        if not width:
            width = 1

        self.system.window.draw_rect(
            self.surface,
            color,
            rect,
            width=width
        )
    # def draw_crazy_cell_borders(self):
    #     rect = self.surface.get_rect()

    #     self.system.window.draw_rect(
    #         self.surface,
    #         self.system.random.choice([white,red,blue]),
    #         rect,
    #         width=1
    #     )

    def update(self):
        pass