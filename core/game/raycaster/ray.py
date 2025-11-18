import math,pygame
from core.game.raycaster.settings import *

def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if(angle < 0):
        angle = (2*math.pi) + angle
    return angle

def distance_between(x1,y1,x2,y2):
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

class Ray:
    def __init__(self,angle,player,map):
        self.ray_angle = normalize_angle(angle)
        self.player = player
        self.map = map
        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.ray_angle < 0.5 * math.pi or self.ray_angle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right
        self.wall_hit_x = 0
        self.wall_hit_y = 0
        self.distance = 0
        self.color_1 = 255
        self.color_2 = 255
        self.color_3 = 255

    def cast(self):
        #horizontal check
        found_h_wall = False
        h_hit_x = 0
        h_hit_y = 0

        first_intersection_x = None
        first_intersection_y = None

        # check vertical direction

        if self.is_facing_up:
            first_intersection_y = ((self.player.y)//TILE_SIZE) * TILE_SIZE - 0.01
        elif self.is_facing_down:
            first_intersection_y = ((self.player.y//TILE_SIZE) * TILE_SIZE) + TILE_SIZE
        
        tangent_value = math.tan(self.ray_angle)

        if tangent_value != 0:
            first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / tangent_value
        else:
            # Handle vertical ray case; use the player's current x position
            first_intersection_x = self.player.x

        # assign current next horizontal points

        next_h_x = first_intersection_x
        next_h_y = first_intersection_y

        xa = 0
        ya = 0

        if self.is_facing_up:
            ya = -TILE_SIZE
        elif self.is_facing_down:
            ya = TILE_SIZE

        if math.tan(self.ray_angle) == 0:
            self.ray_angle += 1
            print("Corrected divide by 0 error")

        xa = ya // math.tan(self.ray_angle)

        #while it's inside the window we check for walls on x axis

        while(next_h_x <= WINDOW_WIDTH and next_h_x >= 0
              and next_h_y <= WINDOW_HEIGHT and next_h_y >=0):
            
            if self.map.has_wall_at(next_h_x,next_h_y):
                found_h_wall = True
                h_hit_x = next_h_x
                h_hit_y = next_h_y
                break
            else:
                next_h_x += xa
                next_h_y += ya

        #test horizontal check

        # self.wall_hit_x = h_hit_x
        # self.wall_hit_y = h_hit_y

        #vertical check

        found_v_wall = False
        v_hit_x = 0
        v_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = ((self.player.x//TILE_SIZE)*TILE_SIZE + 0.01)
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x//TILE_SIZE)*TILE_SIZE -0.01)

        first_intersection_y = self.player.y + (first_intersection_x - self.player.x)*math.tan(self.ray_angle)

        next_v_x = first_intersection_x 
        next_v_y = first_intersection_y

        if self.is_facing_right:
            xa = TILE_SIZE
        elif self.is_facing_left:
            xa = -TILE_SIZE

        ya = xa*math.tan(self.ray_angle)

        if self.is_facing_up and self.player.y < 0:
            return  # Prevent casting rays behind the player
        if self.is_facing_down and self.player.y > WINDOW_HEIGHT:
            return  # Prevent casting rays too far down
        if self.is_facing_left and self.player.x < 0:
            return  # Prevent casting rays to the left
        if self.is_facing_right and self.player.x > WINDOW_WIDTH:
            return  # Prevent casting rays too far right

        #while the rays are inside the window we check the y axis
        while(next_v_x <= WINDOW_WIDTH and next_v_x >= 0
              and next_v_y <= WINDOW_HEIGHT and next_v_y >=0):
            
            if self.map.has_wall_at(next_v_x,next_v_y):
                found_v_wall = True
                v_hit_x = next_v_x
                v_hit_y = next_v_y
                break
            else:
                next_v_x += xa
                next_v_y += ya

        #distance calc

        hor_dist = 0
        vert_dist = 0

        if found_h_wall:
            hor_dist = distance_between(self.player.x,self.player.y,h_hit_x,h_hit_y)
            if self.is_facing_down and h_hit_y < self.player.y:
                hor_dist = float('inf')
            elif self.is_facing_up and h_hit_y > self.player.y:
                hor_dist = float('inf') 
        else:
            hor_dist = 1000
        
        if found_v_wall:
            vert_dist = distance_between(self.player.x,self.player.y,v_hit_x,v_hit_y)
            if self.is_facing_right and v_hit_x < self.player.x:
                vert_dist = float('inf')  # Ignore this hit
            elif self.is_facing_left and v_hit_x > self.player.x:
                vert_dist = float('inf')  # Ignore this hit

        else:
            vert_dist = 9999

        if hor_dist < vert_dist:
            self.wall_hit_x = h_hit_x
            self.wall_hit_y = h_hit_y
            self.distance = hor_dist

            # Get the tile code at the horizontal hit position
            tile_code = self.map.map_grid[int(h_hit_y // TILE_SIZE)][int(h_hit_x // TILE_SIZE)]
            # Check if it's a wall and set the color accordingly
            if self.map.has_wall_at(h_hit_x, h_hit_y):
                tile_info = self.map.tile_key.get(tile_code)
                if tile_info:  # Ensure the tile exists in TILE_KEY
                    if tile_info['type'] == 'wall':
                        self.color_1, self.color_2, self.color_3 = tile_info['color']
            else:
                self.color_1, self.color_2, self.color_3 = 255, 255, 255  # Default color (optional)

        else:
            self.wall_hit_x = v_hit_x
            self.wall_hit_y = v_hit_y
            self.distance = vert_dist

            # Get the tile code at the vertical hit position
            tile_code = self.map.map_grid[int(v_hit_y // TILE_SIZE)][int(v_hit_x // TILE_SIZE)]
            # Check if it's a wall and set the color accordingly
            if self.map.has_wall_at(v_hit_x, v_hit_y):
                tile_info = self.map.tile_key.get(tile_code)
                if tile_info:  # Ensure the tile exists in TILE_KEY
                    if tile_info['type'] == 'wall':
                        self.color_1, self.color_2, self.color_3 = tile_info['color']


        self.distance *= math.cos(self.player.rotation_angle - self.ray_angle)

        # Assuming `self.color` stores the base color for wall type 2
        
            # Apply shading for non-glow walls
        self.color_1 *= (60 / self.distance)
        self.color_2 *= (60 / self.distance)
        self.color_3 *= (60 / self.distance)
        
        if self.color_1 > 255:
            self.color_1 = 255
        elif self.color_1 < 0:
            self.color_1 = 0
        
        if self.color_2 > 255:
            self.color_2 = 255
        elif self.color_2 < 0:
            self.color_2 = 0

        if self.color_3 > 255:
            self.color_3 = 255
        elif self.color_3 < 0:
            self.color_3 = 0

    def draw(self,display):
        
        pygame.draw.line(display,RED,(self.player.x,self.player.y), (self.wall_hit_x,self.wall_hit_y))