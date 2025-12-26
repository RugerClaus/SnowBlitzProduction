import pygame

from helper import get_colors
from config import config

class Window:
    def __init__(self):
        pygame.init()
        self.default_width = 1280
        self.default_height = 820
        self.color = (255,0,0)
        self.width = self.default_width
        self.height = self.default_height
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.set_screen()
        
    def set_screen(self):
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE)
        pygame.display.set_caption(config["TITLE"])

    def get_width(self):
        return self.screen.get_width()
    
    def get_height(self):
        return self.screen.get_height()
    
    def scale(self):
        self.width, self.height = self.screen.get_size()
        self.set_screen()
    
    def scale(self,target_width,target_height):
        self.screen = pygame.display.set_mode((target_width,target_height),pygame.RESIZABLE)

    def get_size(self):
        return self.screen.get_size()

    def timer(self):
        self.clock.tick(self.fps)
    
    def get_current_time(self):
        return pygame.time.get_ticks()

    def default_fill(self):
        self.screen.fill(self.color)

    def fill(self, color,alpha=None):
        if isinstance(color, str):
            color = get_colors(color.lower())
        elif isinstance(color, tuple) and len(color) == 3:
            color = color
            alpha = alpha if alpha is not None else 255
            color = (*color, alpha)
        elif isinstance(color, tuple) and len(color) == 4:
            color = color
        else:
            raise ValueError("fill() only supports RGB or RGBA tuples or color strings")
        self.screen.fill(color)

    def draw_overlay(self, color, alpha):
        overlay = Surface(self.get_width(), self.get_height(), True)
        overlay.fill((*color, alpha))
        return overlay

    def blit(self,surface,destination):
        self.screen.blit(surface,destination)

    def get_screen(self):
        return self.screen
    
    def make_surface(self, width, height, alpha=False):
        return Surface(width, height, alpha)

    def update(self):
        pygame.display.flip()

    def get_fps(self):
        return self.clock.get_fps()
    
class Surface(pygame.Surface):
    def __init__(self, width, height, alpha=False):
        flags = pygame.SRCALPHA if alpha else 0
        super().__init__((width, height), flags)
        self.original_width = width
        self.original_height = height

    def fill(self, color, alpha=None):

        if isinstance(color, str):
            color = get_colors(color.lower())
        elif isinstance(color, tuple) and len(color) == 3:
            color = color
            alpha = alpha if alpha is not None else 255
            color = (*color, alpha)
        elif isinstance(color, tuple) and len(color) == 4:
            color = color
        else:
            raise ValueError("fill() only supports RGB or RGBA tuples or color strings")
        super().fill(color)

    def draw_overlay(self, color, alpha):
        overlay = Surface(self.get_size()[0], self.get_size()[1], True)
        overlay.fill((*color, alpha))
        self.blit(overlay, (0, 0))

    def scale(self):
        self.width, self.height = self.get_size()
    
    def make_surface(self, width, height, alpha=False):
        return Surface(width, height, alpha)
    def scale(self, window_width,window_height):
        # Use pygame.transform.scale to create a new surface with the new size
        scaled_surface = pygame.transform.scale(self, (window_width, window_height))
        
        # Update the surface to point to the scaled surface
        self.blit(scaled_surface, (0, 0))
        
        # Update internal size tracking if needed
        self.original_width = window_width
        self.original_height = window_height

    def make_surface(self, width, height, alpha=False):
        return Surface(width, height, alpha)
