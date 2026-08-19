import os

from core.application.SnowBlitz.world.map import Map

class World:
    def __init__(self, system):
        self.system = system
        self.maps = []

        self.load_map_files()

    def scale(self):
        for map in self.maps:
            map.scale()

    def update(self):
        for map in self.maps:
            map.update()

    def draw(self):
        for map in self.maps:
            map.draw()

    def load_map_files(self):
        path = "enginepersistence/world"

        for filename in os.listdir(path):
            if filename.endswith(".map"):

                filepath = os.path.join(path, filename)

                with open(filepath, "r") as file:
                    cell_map = [
                        [int(cell) for cell in line.strip().strip("[],").split(",")]
                        for line in file
                        if line.strip()
                    ]

                scale = len(cell_map[0]) / 16

                map = Map(self.system, scale)
                map.name = os.path.splitext(filename)[0]

                if map.name == "cloud":
                    map.velocity_x = 0.04

                map.load_cells(cell_map)
                self.maps.append(map)

    def reload_maps(self):
        print("RELOADING MAPS...")
        self.maps.clear()
        self.load_map_files()

    def toggle_map_grid(self, name,color=None,width=None):
        for map in self.maps:
            if map.name == name:
                map.toggle_grid(color,width)
                return