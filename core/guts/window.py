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
    
    def handle_resize(self,e):
        if e.type == pygame.VIDEORESIZE:
            (self.width,self.height) = e.size
            self.set_screen()
    
    def timer(self):
        self.clock.tick(self.fps)
    
    def default_fill(self):
        self.screen.fill(self.color)

    def fill(self, color):
        if isinstance(color, str):
            color = get_colors(color.lower())

        if isinstance(color, tuple) and len(color) == 3:
            self.screen.fill(color)
        else:
            raise ValueError("fill() only supports RGB tuples or color strings")

    def draw_overlay(self, color, alpha):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((*color, alpha))
        self.screen.blit(overlay, (0, 0))

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

    def fill(self, color):
        if isinstance(color, str):
            color = get_colors(color.lower())
        elif isinstance(color, tuple) and len(color) != 3:
            raise ValueError("fill() only supports RGB tuples or color strings")
        
        super().fill(color)

    def draw_overlay(self, color, alpha):
        overlay = Surface(self.get_size()[0], self.get_size()[1], True)
        overlay.fill((*color, alpha))
        self.blit(overlay, (0, 0))
    