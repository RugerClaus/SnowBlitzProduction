import pygame
from enum import Enum, auto
from core.ui.font import FontEngine

class SizeBar(Enum):
    BOTTOM = auto()
    TOP = auto()

class SizeBarManager:
    def __init__(self, window, player, start_time):
        self.location = SizeBar.BOTTOM
        self.window = window
        self.player = player
        self.bar_width = self.window.get_width()  # Start with the full window width
        self.bar_height = 20  # Default height for top/bottom bars
        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)  # Using your custom surface creation
        self.rect_position = (0, 0)
        self.start_time = start_time
        self.font = FontEngine(35).font

    def scale(self):
        # Recalculate the position and size of the progress bar based on window resizing
        if self.location == SizeBar.BOTTOM:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, self.window.get_height() - self.bar_height)
        elif self.location == SizeBar.TOP:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, 0)

        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)
        self.draw_player_info()

    def toggle_location(self):
        if self.location == SizeBar.BOTTOM:
            self.location = SizeBar.TOP
        else:
            self.location = SizeBar.BOTTOM

    def draw_player_info(self):
        elapsed_ms = pygame.time.get_ticks() - self.start_time
        seconds = (elapsed_ms // 1000) % 60
        minutes = (elapsed_ms // 60000)
        
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_text, True, (255, 255, 255))
        
        size_text = f"Size: {round(self.player.diam)}"
        size_surface = self.font.render(size_text, True, (255, 255, 255))

        level_text = f"Level: {self.player.current_level}"
        level_surface = self.font.render(level_text, True, (255,255,255))

        size_to_level_up_text = f"Size to level up: {self.player.level_up_size}"
        size_to_level_up_surface = self.font.render(size_to_level_up_text, True, (255,255,255))

        score_text = f"Score: {self.player.score}"
        score_surface = self.font.render(score_text, True, (255,255,255))

        self.window.blit(time_surface, (10,60))
        self.window.blit(size_surface, (10,90))
        self.window.blit(level_surface, (10,120))
        self.window.blit(size_to_level_up_surface, (self.window.get_width() - size_to_level_up_surface.get_rect().width - 10,60))
        self.window.blit(score_surface, (self.window.get_width() - score_surface.get_rect().width - 10,90))

    def draw(self):

        self.draw_player_info()

        if self.location in [SizeBar.TOP, SizeBar.BOTTOM]:
            size_avg = self.player.diam
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_width = int(self.bar_width * progress)
            fill_width = max(fill_width, 1)

            self.surface.fill((0, 0, 0))  # Fill with black
            outline_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)  # Outline of the bar

            fill_color = (
                max(0, min(255, int(255 * (1 - progress)))),  # Clamp Red value
                max(0, min(255, int(255 * progress))),        # Clamp Green value
                0                                              # Blue stays at 0
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
