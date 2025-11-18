import pygame
from core.game.raycaster.settings import *

class Map:
    def __init__(self,player):
        self.player = player
        self.map_grid = []
        self.tile_key = TILE_KEY
        self.maps = {
           0: [
                ['W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F3', 'F1', 'F1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1'],
                ['W1', 'W1', 'W1', 'W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1', 'W1', 'W1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1', 'F1', 'F1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F1', 'W1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'F1', 'W1'],
                ['W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1']
            ],
            1: [
                ['W1', 'W2', 'W2', 'W2', 'W1', 'W1', 'W1', 'W1', 'W2', 'W2', 'W2', 'W2', 'W1', 'W1', 'W1'],
                ['W1', 'F2', 'F2', 'F2', 'F1', 'W1', 'F2', 'F2', 'F2', 'F2', 'F1', 'F2', 'F2', 'F2', 'W1'],
                ['W1', 'F1', 'F1', 'F1', 'F2', 'F2', 'F2', 'F2', 'F1', 'F2', 'F2', 'F1', 'F2', 'F2', 'W1'],
                ['W1', 'F1', 'F2', 'F1', 'F1', 'F1', 'F2', 'F1', 'F1', 'F1', 'F1', 'F2', 'F2', 'F2', 'W1'],
                ['W1', 'W2', 'W2', 'W2', 'F2', 'F2', 'F1', 'F2', 'F2', 'F1', 'W1', 'W1', 'W2', 'W2', 'W1'],
                ['W1', 'F1', 'F2', 'F1', 'F2', 'W1', 'F1', 'F1', 'F2', 'F2', 'F1', 'F1', 'F1', 'F2', 'W1'],
                ['W1', 'F1', 'F1', 'F2', 'F1', 'W1', 'F1', 'F1', 'F1', 'F2', 'F2', 'W1', 'F2', 'F2', 'W1'],
                ['W1', 'F2', 'F2', 'F1', 'F1', 'W1', 'F2', 'F1', 'F2', 'F1', 'F1', 'F2', 'F2', 'F1', 'W1'],
                ['W1', 'F2', 'F2', 'F1', 'F2', 'W1', 'F2', 'F2', 'F2', 'F1', 'F1', 'F2', 'F1', 'F2', 'W1'],
                ['W1', 'W2', 'W2', 'W2', 'W1', 'W2', 'W1', 'W2', 'W2', 'W1', 'W1', 'W1', 'W1', 'W1', 'W1']
            ],
        
        }

    def has_wall_at(self, x, y):
        tile_code = self.map_grid[int(y // TILE_SIZE)][int(x // TILE_SIZE)]
        return TILE_KEY[tile_code]['type'] == 'wall' 

    def update(self):
        # Dynamically load map based on player's level
        level = self.player.level
        if level in self.maps:
            self.map_grid = self.maps[level]
        else:
            print("Level not available!")
            level = 0
            self.map_grid = self.maps[level]


    def draw(self, display):
        display.fill((0, 0, 0))  # Clear the screen

        for i in range(len(self.map_grid)):
            for j in range(len(self.map_grid[0])):
                tile_x = j * TILE_SIZE // 4
                tile_y = i * TILE_SIZE // 4

                tile_code = self.map_grid[i][j]  # Get the tile code
                tile_color = TILE_KEY.get(tile_code, {}).get('color', (0, 0, 0))

                # Draw the tile with the appropriate color
                pygame.draw.rect(display, tile_color, (tile_x, tile_y, TILE_SIZE // 4 - 1, TILE_SIZE // 4 - 1))
