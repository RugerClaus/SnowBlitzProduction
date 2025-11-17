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

    def crosshair(self,display):
        pygame.draw.rect(display,WHITE,(WINDOW_WIDTH//2-5,WINDOW_HEIGHT//2,12,2)) #horizontal crosshair
        pygame.draw.rect(display,WHITE,(WINDOW_WIDTH//2,WINDOW_HEIGHT//2-5,2,12)) #vertical crosshair


# this is the draw method that handles all on screen action

    def draw(self, display):
        for i, ray in enumerate(self.rays):
            # Calculate line height based on the distance of the ray
            line_height = (TILE_SIZE / ray.distance) * 831
            draw_begin = (WINDOW_HEIGHT / 2 - line_height / 2)

            # Draw the ray on screen
            pygame.draw.rect(display, (ray.color_1,ray.color_2,ray.color_3), (i * RES, draw_begin, RES, line_height))
        
        # Draw the crosshair after all rays have been drawn
        self.crosshair(display)
