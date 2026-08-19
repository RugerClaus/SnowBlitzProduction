
from core.util.colors import *
from core.application.SnowBlitz.world.cell import Cell

class Map:
    def __init__(self,system,scale):
        self.system = system

        self.cells = []

        self.grid_scale = scale
        self.scale()

        self.cell_data_map = {
            0: [None],
            1: [green],
            2: [yellow],
            3: [white]
        }

        self.x = 0
        self.y = 0
        self.velocity_x = 0
        self.velocity_y = 0

    def scale(self):

        self.rows = int(9 * self.grid_scale)
        self.columns = int(16 * self.grid_scale)

        for cell in self.cells:
            cell.scale()

    def update(self):
        dt = self.system.time.delta_time()

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if self.x >= 1:
            self.x -= 1
        elif self.x <= -1:
            self.x += 1

        for cell in self.cells:
            cell.update()

    def draw(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        offset_x = self.x * ww
        offset_y = self.y * wh

        for cell in self.cells:
            rect = cell.rect.move(offset_x, offset_y)
            self.system.window.blit(cell.surface, rect)

            rect = cell.rect.move(offset_x - ww, offset_y)
            self.system.window.blit(cell.surface, rect)

            rect = cell.rect.move(offset_x + ww, offset_y)
            self.system.window.blit(cell.surface, rect)

    def _get_cell_data(self,id): # returns a list of values that make up each cell type
        for key,value in self.cell_data_map.items():
            if key == id:
                return value

    def load_cells(self, cell_map):
        self.cells.clear()
        cell_width = 1 / self.columns
        cell_height = 1 / self.rows

        for index, cell_id in enumerate(cell_map):
            x = index % self.columns
            y = index // self.columns

            position = (
                (x + 0.5) * cell_width,
                (y + 0.5) * cell_height
            )

            size = (
                cell_width,
                cell_height
            )

            cell = Cell(
                self.system,
                self._get_cell_data(cell_id)[0],
                size,
                position
            )

            self.cells.append(cell)