import pygame
from core.game.raycaster.settings import *



class Map:
    def __init__(self,player):
        self.player = player
        self.map_grid = []
        self.maps = {
           0: [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],                # 2 is goal block
            [1,0,0,2,0,0,0,0,0,0,0,0,0,0,1],                # 1 is wall
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],                # 0 is floor
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,0,0,0,0,0,0,0,1,1,1,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        1: [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],                # 2 is goal block
            [1,0,0,0,0,1,0,0,1,0,0,0,0,0,1],                # 1 is wall
            [1,0,1,1,0,0,0,0,1,0,1,1,1,1,1],                # 0 is floor
            [1,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
            [1,1,1,1,0,1,0,0,1,0,0,1,1,1,1],
            [1,0,0,0,0,1,0,0,1,1,0,0,0,0,1],
            [1,0,0,0,0,1,0,0,0,1,0,1,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,1,0,0,1],
            [1,0,0,0,0,1,0,0,0,0,0,1,2,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        
        2: [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],                # 2 is goal block
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],                # 1 is wall
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],                # 0 is floor
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,0,0,0,1,1,1,1,1,1],
            [1,0,0,2,0,1,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,0,0,0,0,0,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        
        }

    def has_wall_at(self,x,y):
        return self.map_grid[int(y//TILE_SIZE)][int(x//TILE_SIZE)] #converting pixel to tile

    def update(self):
        if self.player.level == 1:
            self.map_grid = self.maps[0]
        if self.player.level == 2:
            self.map_grid = self.maps[1]
        if self.player.level == 3:
            self.map_grid = self.maps[2]

    def draw(self,display):
        for i in range(len(self.map_grid)):
            for j in range(len(self.map_grid[0])):
                tile_x = j * TILE_SIZE // 4
                tile_y = i * TILE_SIZE // 4 #pixel coordinates to render the environment

                if self.map_grid[i][j] == 0:
                    pygame.draw.rect(display,WHITE,(tile_x,tile_y,TILE_SIZE//4-1,TILE_SIZE//4-1))
                elif self.map_grid[i][j] == 1:
                    pygame.draw.rect(display,GREY,(tile_x,tile_y,TILE_SIZE//4-1,TILE_SIZE//4-1))
                elif self.map_grid[i][j] == 2:
                    pygame.draw.rect(display,PURPLE,(tile_x,tile_y,TILE_SIZE//4-1,TILE_SIZE//4-1))
