import math

class Entity:
    def __init__(self, x, y, radius=6, speed=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.rotation_angle = 0


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