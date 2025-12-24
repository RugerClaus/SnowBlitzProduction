import pygame
from enum import Enum, auto

class SizeBar(Enum):
    LEFT = auto()
    RIGHT = auto()
    BOTTOM = auto()
    TOP = auto()

class SizeBarManager:
    def __init__(self, window, player):
        self.location = SizeBar.TOP
        self.window = window
        self.player = player
        self.bar_width = self.window.get_width()  # Make sure the bar takes up the full screen width
        self.bar_height = 20
        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)
        self.rect_position = (0, 0)
        self.scale()

    def scale(self):
        rect = self.surface.get_rect()
        # Position the bar at the top or bottom center of the screen
        if self.location == SizeBar.BOTTOM:
            rect.center = (self.window.get_width() // 2, self.window.get_height() - 50)
        elif self.location == SizeBar.TOP:
            rect.center = (self.window.get_width() // 2, rect.height // 2)
        elif self.location == SizeBar.LEFT:
            rect.center = (rect.width // 2, self.window.get_height() // 2)
        elif self.location == SizeBar.RIGHT:
            rect.center = (self.window.get_width() - rect.width // 2, self.window.get_height() // 2)

        self.rect_position = rect.topleft

    def draw(self):
        if self.location in [SizeBar.TOP, SizeBar.BOTTOM]:
            size_avg = self.player.diam
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_width = int(self.bar_width * progress)
            fill_width = max(fill_width, 1)

            self.surface.fill((0, 0, 0))  # Fill the surface with black
            outline_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)

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

        elif self.location in [SizeBar.LEFT, SizeBar.RIGHT]:
            bar_width = 20
            bar_height = self.window.get_height() // 2
            size_avg = (self.player.width + self.player.height) / 2
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_height = bar_height * progress

            self.surface.fill((0, 0, 0))  # Fill with black
            outline_rect = pygame.Rect(50, self.window.get_height() - bar_height - 50, bar_width, bar_height)

            fill_rect = pygame.Rect(
                outline_rect.left + 2,
                outline_rect.bottom - fill_height + 2,  # Start from bottom of bar
                bar_width - 4,                         # Padding
                fill_height - 4 if fill_height >= 4 else 0
            )

            fill_color = (
                int(255 * (1 - progress)),  # Red to green color transition
                int(255 * progress),
                0
            )

            pygame.draw.rect(self.surface, fill_color, fill_rect)
            pygame.draw.rect(self.surface, (255, 255, 255), outline_rect, 2)  # White border

        self.window.blit(self.surface, self.rect_position)

    def update(self):
        self.scale()
        self.draw()
