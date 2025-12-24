import pygame
from enum import Enum, auto

class SizeBar(Enum):
    BOTTOM = auto()
    TOP = auto()

class SizeBarManager:
    def __init__(self, window, player):
        self.location = SizeBar.BOTTOM
        self.window = window
        self.player = player
        self.bar_width = self.window.get_width()  # Start with the full window width
        self.bar_height = 20  # Default height for top/bottom bars
        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)  # Using your custom surface creation
        self.rect_position = (0, 0)

    def scale(self):
        # Recalculate the position and size of the progress bar based on window resizing
        if self.location == SizeBar.BOTTOM:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, self.window.get_height() - self.bar_height)
        elif self.location == SizeBar.TOP:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, 0)

        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)

    def draw(self):
        if self.location in [SizeBar.TOP, SizeBar.BOTTOM]:
            size_avg = self.player.diam
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_width = int(self.bar_width * progress)
            fill_width = max(fill_width, 1)

            self.surface.fill((0, 0, 0))  # Fill with black
            outline_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)  # Outline of the bar

            fill_color = (
                int(255 * (1 - progress)),  # Red decreases
                int(255 * progress),        # Green increases
                0                            # Blue stays at 0
            )
            fill_rect = pygame.Rect(
                outline_rect.left + 2,       
                outline_rect.top + 2,        
                fill_width - 4,              # Padding to prevent touching edges
                self.bar_height - 4          # Padding
            )
            pygame.draw.rect(self.surface, fill_color, fill_rect)
            pygame.draw.rect(self.surface, (255, 255, 255), outline_rect, 2)  # White border

        self.window.blit(self.surface, self.rect_position)

    def update(self):
        self.scale()
