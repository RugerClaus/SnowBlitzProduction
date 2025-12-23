import pygame
from enum import Enum,auto

class SizeBar(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTTOM = auto()
    TOP = auto()

class SizeBarManager:
    def __init__(self,window,player):
        self.location = SizeBar.BOTTOM
        self.window = window
        self.player = player
        self.surface = self.window.make_surface(self.window.get_width()//2,20,True)

    def draw(self):
        if self.location == SizeBar.BOTTOM:
            bar_width,bar_height = self.window.get_width()//2,20
            size_avg = (self.player.diam * 2)//2
            progress = min(size_avg / self.player.level_up_size,1.0)
            fill_width = int(bar_width * progress)

            outline_rect = pygame.Rect(self.window.get_width()//4,self.window.get_height()-50,bar_width,bar_height)
            fill_rect = pygame.Rect(self.window.get_width()//4,self.window.get_height()-50,fill_width,bar_height)
            fill_color = (
                int(255 * (1 - progress)),
                int(255 * progress),
                0
            )
            pygame.draw.rect(self.surface,fill_color,fill_rect)
            pygame.draw.rect(self.surface,(255,255,255),outline_rect,2)
            self.window.blit(self.surface,(self.window.get_width()//4,self.window.get_height()-50))

    def update(self):
        current_width, current_height = self.window.get_size()
        if (self.surface.get_width(), self.surface.get_height()) != (current_width, current_height):
            self.surface = self.window.make_surface((current_width, current_height), True)
            self.rect = self.surface.get_rect()