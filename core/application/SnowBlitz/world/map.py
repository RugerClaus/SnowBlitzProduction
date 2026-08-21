from helper import sine
from core.util.colors import *
from core.application.SnowBlitz.world.cell import Cell

from core.application.SnowBlitz.world.data_map import cell_data_map


class Map:
    def __init__(self,system,scale,environment=None):
        self.system = system
        self.name = None

        self.cell_map = []
        self.cells = []

        self.grid_scale = scale
        self.scale()

        self.cell_data_map = cell_data_map

        self.x = 0
        self.y = 0
        self.velocity_x = 0
        self.velocity_y = 0

        self.draw_grid = False
        self.grid_color = white
        self.grid_line_width = 1
        self.environment = environment

        self.layer_surface = None
        self.layer_size = None
        self.layer_dirty = True


    def get_cell_rect(self, column, row):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        left = round(column * ww / self.columns)
        right = round((column + 1) * ww / self.columns)

        top = round(row * wh / self.rows)
        bottom = round((row + 1) * wh / self.rows)

        return self.system.window.Rect(left,top,right - left,bottom - top)

    def create_layer_surface(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        self.layer_surface = self.system.window.make_surface(
            ww,
            wh,
            True
        )

        self.layer_size = (ww, wh)
        self.layer_dirty = True


    def render_layer(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        # Fullscreen/window resize detection.
        if (
            self.layer_surface is None
            or self.layer_size != (ww, wh)
        ):
            self.create_layer_surface()

        if not self.layer_dirty:
            return

        self.layer_surface.fill((0, 0, 0, 0))

        for index, cell in enumerate(self.cells):

            column = index % self.columns
            row = index // self.columns

            rect = self.get_cell_rect(column, row)

            if cell.color:
                self.layer_surface.fill(
                    cell.color,
                    rect
                )

        if self.draw_grid:
            self.render_debug_grid()

        self.layer_dirty = False



    def scale(self, scale=None):
        if scale is not None:
            scale = int(scale)

        else:
            scale = int(self.grid_scale)

        if scale < 1:
            raise ValueError("Map scale must be >= 1")

        self.grid_scale = scale

        self.rows = 9 * scale
        self.columns = 16 * scale


    def update_cell_colors(self):
        if self.environment is None:
            return

        brightness = self.environment.day_cycle.brightness

        ambient = 0.35
        light = ambient + ((1.0 - ambient) * brightness)

        for cell in self.cells:
            if not cell.properties.get("receives_light", False):
                continue

            base_color = cell.data.get("color")

            if base_color is None:
                continue

            color = tuple(
                int(channel * light)
                for channel in base_color
            )

            cell.set_color(color)

        self.layer_dirty = True

    def update(self):
        dt = self.system.time.delta_time()

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        if self.x >= 1:
            self.x -= 1
        elif self.x <= -1:
            self.x += 1

        self.update_cell_colors()

        for cell in self.cells:
            cell.update()

    def draw(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        self.render_layer()

        offset_x = round(self.x * ww)
        offset_y = round(self.y * wh)

        offsets = (
            (offset_x - ww, offset_y),
            (offset_x, offset_y),
            (offset_x + ww, offset_y),
        )

        for x, y in offsets:
            self.system.window.blit(
                self.layer_surface,
                (x, y)
            )

    def render_debug_grid(self):
        ww = self.system.window.get_width()
        wh = self.system.window.get_height()

        color = self.grid_color or white
        width = self.grid_line_width or 1

        for column in range(self.columns + 1):
            x = round(column * ww / self.columns)

            self.system.window.draw_line(
                self.layer_surface,
                (x, 0),
                (x, wh),
                color,
                width
            )

        for row in range(self.rows + 1):
            y = round(row * wh / self.rows)

            self.system.window.draw_line(
                self.layer_surface,
                (0, y),
                (ww, y),
                color,
                width
            )

    def toggle_grid(self, grid_color=None, grid_line_width=None):
        if grid_color is not None:
            self.grid_color = grid_color

        if grid_line_width is not None:
            self.grid_line_width = grid_line_width

        self.draw_grid = not self.draw_grid
        self.layer_dirty = True

        print("toggling debug grid:", self.draw_grid)

    def _get_cell_data(self, cell_type):
        return self.cell_data_map.get(cell_type)

    def load_cells(self, cell_map):
        self.cells.clear()

        if not cell_map:
            raise ValueError("Map cannot be empty")

        source_rows = len(cell_map)
        source_columns = len(cell_map[0])

        if any(len(row) != source_columns for row in cell_map):
            raise ValueError("All map rows must have the same length")

        # Scale the base map if necessary.
        if (
            source_rows != self.rows
            or source_columns != self.columns
        ):
            cell_map = self.scale_map(cell_map)

        if len(cell_map) != self.rows:
            raise ValueError(
                f"Expected {self.rows} rows, got {len(cell_map)}"
            )

        if len(cell_map[0]) != self.columns:
            raise ValueError(
                f"Expected {self.columns} columns, got {len(cell_map[0])}"
            )

        self.cell_map = cell_map

        cell_width = 1 / self.columns
        cell_height = 1 / self.rows

        for y, row in enumerate(cell_map):
            for x, cell_id in enumerate(row):

                cell_data = self._get_cell_data(cell_id)

                if cell_data is None:
                    raise ValueError(
                        f"Unknown cell type: {cell_id}"
                    )

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
                    size,
                    position,
                    cell_data
                )

                self.cells.append(cell)

        self.layer_dirty = True


    def scale_map(self, cell_map):
        scaled = []

        source_rows = len(cell_map)

        if source_rows == 0:
            raise ValueError("Cannot scale an empty map")

        source_columns = len(cell_map[0])

        if source_columns == 0:
            raise ValueError("Cannot scale an empty map")

        if any(len(row) != source_columns for row in cell_map):
            raise ValueError("All map rows must have the same length")

        scale = int(self.grid_scale)

        for row in cell_map:
            expanded_row = []

            for cell in row:
                expanded_row.extend([cell] * scale)

            for _ in range(scale):
                scaled.append(expanded_row.copy())

        return scaled
