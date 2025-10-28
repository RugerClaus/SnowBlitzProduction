import pygame

class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def update(self, target):
        self.offset_x = target.x_pos - self.width // 2
        self.offset_y = target.y_pos - self.height // 2

        self.offset_x = max(0, self.offset_x)
        self.offset_y = max(0, self.offset_y)

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)
    
    def in_view(self, x, y, tile_size):
        cam_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        return cam_rect.colliderect(tile_rect)
