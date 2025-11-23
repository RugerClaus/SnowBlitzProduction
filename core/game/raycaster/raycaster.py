import pygame,math
from core.game.raycaster.settings import *
from core.game.raycaster.ray import Ray

class Raycaster:
    def __init__(self,player,map):
        self.rays = []
        self.player = player
        self.map = map

    def cast_all_rays(self): # casts all rays from rays[**]
        self.rays = []
        ray_angle = (self.player.rotation_angle - FOV/2) 
        for i in range(NUM_RAYS):
            ray = Ray(ray_angle,self.player,self.map)
            ray.cast()
            self.rays.append(ray)

            ray_angle += FOV / NUM_RAYS

# this is the draw method that handles all on screen action

    def draw(self, display):
        for i, ray in enumerate(self.rays):
            # Calculate line height based on the distance of the ray
            line_height = (TILE_SIZE / ray.distance) * 831
            draw_begin = (WINDOW_HEIGHT / 2 - line_height / 2)

            # Draw the ray on screen
            pygame.draw.rect(display, (ray.color_1,ray.color_2,ray.color_3), (i * RES, draw_begin, RES, line_height))
        
        # Draw the crosshair after all rays have been drawn
        self.player.crosshair(display)
        self.player.draw_gun(display)

    def draw_floor(self, display):
        half_height = WINDOW_HEIGHT / 2

        for i, ray in enumerate(self.rays):
            line_height = (TILE_SIZE / ray.distance) * 831
            draw_begin = half_height - line_height / 2
            draw_end = draw_begin + line_height

            y = int(draw_end)
            while y < WINDOW_HEIGHT:
                distance = (WINDOW_HEIGHT / (2 * (y - half_height)))  
                distance *= math.cos(ray.ray_angle - self.player.rotation_angle)  

                color = (128, 100, 128)

                pygame.draw.rect(display, color, (i * RES, y, RES, RES))
                y += RES
