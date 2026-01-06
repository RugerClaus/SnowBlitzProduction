import pygame
from enum import Enum, auto
from core.ui.font import FontEngine
from helper import read_constant_from_file

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
        self.score_font = FontEngine(60).font

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

        # Prepare text
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_text, True, (255, 255, 255))

        size_text = f"Size: {round(self.player.diam)}"
        size_surface = self.font.render(size_text, True, (255, 255, 255))

        level_text = f"Level: {self.player.current_level}"
        level_surface = self.score_font.render(level_text, True, (255,255,255))

        size_to_level_up_text = f"Size to level up: {self.player.level_up_size}"
        size_to_level_up_surface = self.font.render(size_to_level_up_text, True, (255,255,255))

        score_text = f"Score: {self.player.score}"
        score_surface = self.score_font.render(score_text, True, (255,255,0))

        high_score_text = f"High Score: {self.player.current_high_score}"
        high_score_surface = self.score_font.render(high_score_text, True, (255,74,128))

        line_spacing = 20

        if self.location == SizeBar.TOP:
            top_y = self.bar_height + 10
            self.window.blit(time_surface, (10, top_y))
            self.window.blit(size_surface, (10, top_y + line_spacing))
            self.window.blit(high_score_surface, (self.window.get_width() - high_score_surface.get_rect().width - 10, top_y))
            self.window.blit(score_surface, (self.window.get_width() - score_surface.get_rect().width - high_score_surface.get_rect().width - 40, top_y))
            self.window.blit(level_surface, (self.window.get_width() - level_surface.get_rect().width - score_surface.get_rect().width - score_surface.get_rect().right * 2, top_y))
            self.window.blit(size_to_level_up_surface, (time_surface.get_rect().right + 30, top_y))

        elif self.location == SizeBar.BOTTOM:
            bottom_y = self.window.get_height() - self.bar_height - 80 
            self.window.blit(time_surface, (10, bottom_y + line_spacing))
            self.window.blit(size_surface, (10, bottom_y + line_spacing * 2))
            self.window.blit(size_to_level_up_surface, (10, bottom_y + line_spacing * 3))
            self.window.blit(high_score_surface, (self.window.get_width() - high_score_surface.get_rect().width - 10, bottom_y + line_spacing * 2))
            self.window.blit(score_surface, (self.window.get_width() - score_surface.get_rect().width - high_score_surface.get_rect().width - 40, bottom_y + line_spacing * 2))
            self.window.blit(level_surface, (self.window.get_width() - level_surface.get_rect().width - score_surface.get_rect().width - score_surface.get_rect().right * 2, bottom_y + line_spacing * 2))

    def draw(self):

        self.surface.fill((0, 0, 0))

        if self.location in [SizeBar.TOP, SizeBar.BOTTOM]:
            size_avg = self.player.diam
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_width = int(self.bar_width * progress)
            fill_width = max(fill_width, 1)

            outline_rect = pygame.Rect(0, 0, self.bar_width, self.bar_height)

            fill_color = (
                max(0, min(255, int(255 * (1 - progress)))),
                max(0, min(255, int(255 * progress))),
                0
            )
            fill_rect = pygame.Rect(
                outline_rect.left + 2,       
                outline_rect.top + 2,        
                fill_width - 4,
                self.bar_height - 4
            )

            pygame.draw.rect(self.surface, fill_color, fill_rect)
            pygame.draw.rect(self.surface, (255, 255, 255), outline_rect, 2)

        self.draw_player_info()

        self.window.blit(self.surface, self.rect_position)

    def update(self):
        self.scale()
