
from core.util.colors import *
from core.application.SnowBlitz.world.cell import Cell

class Map:
    def __init__(self,system,scale):
        self.system = system

        self.name = None

        self.cell_map = []
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

        self.draw_grid = False
        self.grid_color = None
        self.grid_line_width = None

    def get_cell_rect(self, column, row):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        left = round(column * ww / self.columns)
        right = round((column + 1) * ww / self.columns)

        top = round(row * wh / self.rows)
        bottom = round((row + 1) * wh / self.rows)

        return self.system.window.Rect(
            left,
            top,
            right - left,
            bottom - top
        )

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

        offset_x = round(self.x * ww)
        offset_y = round(self.y * wh)

        for index, cell in enumerate(self.cells):

            column = index % self.columns
            row = index // self.columns

            rect = self.get_cell_rect(column, row)

            if (
                cell.surface is None
                or cell.surface.get_width() != rect.width
                or cell.surface.get_height() != rect.height
            ):
                cell.scale(rect.width, rect.height)

            rect.x += offset_x
            rect.y += offset_y

            self.system.window.blit(cell.surface, rect)

            rect = self.get_cell_rect(column, row)
            rect.x += offset_x - ww
            rect.y += offset_y

            self.system.window.blit(cell.surface, rect)

            rect = self.get_cell_rect(column, row)
            rect.x += offset_x + ww
            rect.y += offset_y

            self.system.window.blit(cell.surface, rect)

            if self.draw_grid:
                cell.draw_debug_border(
                    self.grid_color,
                    self.grid_line_width
                )

    def toggle_grid(self, grid_color=None, grid_line_width=None):
        self.grid_color = grid_color
        self.grid_line_width = grid_line_width
        self.draw_grid = not self.draw_grid

        if not self.draw_grid:
            for cell in self.cells:
                cell.scale()

    def _get_cell_data(self,id): # returns a list of values that make up each cell type may be a dict in the future
        for key,value in self.cell_data_map.items():
            if key == id:
                return value

    def load_cells(self, cell_map):
        self.cells.clear()

        if len(cell_map) != self.rows or len(cell_map[0]) != self.columns:
            cell_map = self.scale_map(cell_map)

        cell_width = 1 / self.columns
        cell_height = 1 / self.rows

        for y, row in enumerate(cell_map):
            for x, cell_id in enumerate(row):

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

    def scale_map(self, cell_map):
        scaled = []

        source_columns = 16
        source_rows = 9

        for y in range(source_rows):
            row = cell_map[y * source_columns:(y + 1) * source_columns]

            expanded_row = []

            for cell in row:
                expanded_row.extend([cell] * self.grid_scale)

            for _ in range(self.grid_scale):
                scaled.extend(expanded_row)

        return scaled