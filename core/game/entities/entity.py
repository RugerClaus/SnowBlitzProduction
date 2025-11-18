import math
from random import randint
from core.game.raycaster.settings import COLS,ROWS,TILE_SIZE

class Entity:
    def __init__(self, x, y, radius=6, speed=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.rotation_angle = 0


    def find_safe_spawn(self, game_map):
        for _ in range(150):
            random_col = randint(0, COLS - 1)
            random_row = randint(0, ROWS - 1)

            # Check if the tile is empty (0)
            if game_map.map_grid[random_row][random_col] == 0:
                # Ensure the surrounding tiles are also empty (not walls)
                # Check surrounding tiles: top, bottom, left, right (if within bounds)
                if (random_row > 0 and game_map.map_grid[random_row - 1][random_col] == 0) and \
                (random_row < ROWS - 1 and game_map.map_grid[random_row + 1][random_col] == 0) and \
                (random_col > 0 and game_map.map_grid[random_row][random_col - 1] == 0) and \
                (random_col < COLS - 1 and game_map.map_grid[random_row][random_col + 1] == 0):
                    # Spawn the player at this location (convert tile index to pixel)
                    self.x = random_col * TILE_SIZE
                    self.y = random_row * TILE_SIZE
                    self.walk_direction = 0
                    self.turn_direction = 0
                    return  # Exit once a valid spawn point is found

        # If no valid spot was found after 102 tries, default to the center of the map
        self.x = (COLS // 2) * TILE_SIZE
        self.y = (ROWS // 2) * TILE_SIZE

    def will_collide(self, new_x, new_y, game_map):
        for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
            cx = new_x + math.cos(angle) * self.radius
            cy = new_y + math.sin(angle) * self.radius

            if game_map.has_wall_at(cx, cy):
                return True
        return False

    def update(self, game_map):
        pass  # Overridden by Player or NPC subclasses

    def draw(self,display):
        pass