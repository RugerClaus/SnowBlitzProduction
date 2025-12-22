import pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity

class Player(Entity):
    def __init__(self, board_surface):
        self.base_size = 10                # radius in logical pixels
        self.board_surface = board_surface
        x = board_surface.get_width() // 2
        y = board_surface.get_height() - board_surface.get_height() // 8
        super().__init__(x, y, EntityType.PLAYER, self.base_size)
        diam = self.base_size * 2
        self.surface = self.board_surface.make_surface(diam, diam, True)
        self.rect = self.surface.get_rect()
        
        self.rect.center = (int(self.x), int(self.y))

    def update_y(self):
        # keep y relative to board height
        self.y = self.board_surface.get_height() - self.board_surface.get_height() // 8
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        
        self.update_y()

    def draw(self):
        # clear small surface (preserve alpha)
        self.surface.fill((0, 0, 0, 0))
        # draw circle centered inside the small surface using local coords
        pygame.draw.circle(self.surface, (255, 255, 255),
                           (self.base_size, self.base_size), self.base_size)
        # ensure rect is placed at the player's world position
        self.rect.center = (int(self.x), int(self.y))
        # blit player surface onto board surface
        self.board_surface.blit(self.surface, self.rect.topleft)
