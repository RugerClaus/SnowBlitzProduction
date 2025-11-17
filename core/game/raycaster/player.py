import pygame
import math
from core.game.raycaster.settings import *


class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2

        self.map_x = WINDOW_WIDTH / 4
        self.map_y = WINDOW_HEIGHT / 4
        self.radius = 6
        self.turn_direction = 0 # -1 left 1 right 0 center float
        self.walk_direction = 0 # 1 player moving forward -1 player move backward
        self.speed = 2.5
        self.rotation_speed = 2 * (math.pi/180)
        self.rotation_angle = -45*(math.pi/180)

        self.level = 1

    def will_collide(self, new_x, new_y, game_map):
        #check all cardinal directions. this idea should have been obvious for circle collision and I can just use math.pi to calculate 
        # the trajectory of every angle around the player and determine if the player hits a wall that way
        # das is good
        for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
            check_x = new_x + math.cos(angle) * self.radius
            check_y = new_y + math.sin(angle) * self.radius

            if game_map.has_wall_at(check_x, check_y) == 1:
                return True
            elif game_map.has_wall_at(check_x,check_y) == 2:
                self.level += 1
                self.x = WINDOW_WIDTH / 2
                self.y = WINDOW_HEIGHT / 2
                return True
        return False


    def update(self,game_map):

        keys = pygame.key.get_pressed()

        self.turn_direction = 0 # 0 is not turning
        self.walk_direction = 0 # is not moving

        if keys[pygame.K_d]:
            self.turn_direction = 1                     #this stuff is all for setting the direction we walk.
        if keys[pygame.K_a]:                               # this is not an actual 3D space, it's a 2D one we're projecting
            self.turn_direction = -1                    # the result of this projection will be a player walking in a seemingly 3D space
        if keys[pygame.K_w]:                            # hopefully we can pull it off with a tutorial, but i'll see. sometimes i fuck things up
            self.walk_direction = 1
        if keys[pygame.K_s]:
            self.walk_direction = -1
        
        move_step = self.walk_direction * self.speed

        self.rotation_angle += self.turn_direction * self.rotation_speed
        new_x = self.x + math.cos(self.rotation_angle) * move_step
        new_y = self.y + math.sin(self.rotation_angle) * move_step


        if not self.will_collide(new_x, new_y, game_map):
            self.x = new_x
            self.y = new_y

        #handle player on minimap

        self.map_x = max(0, min((self.x / WINDOW_WIDTH) * (WINDOW_WIDTH // 4), WINDOW_WIDTH // 4))
        self.map_y = max(0, min((self.y / WINDOW_HEIGHT) * (WINDOW_HEIGHT // 4), WINDOW_HEIGHT // 4))


    def draw(self, display):


        pygame.draw.circle(display,GREEN,(self.map_x,self.map_y), self.radius)

        pygame.draw.line(display,RED,(self.map_x,self.map_y), (self.map_x + math.cos(self.rotation_angle)*(self.radius*2),self.map_y+math.sin(self.rotation_angle)*(self.radius*2)))

    