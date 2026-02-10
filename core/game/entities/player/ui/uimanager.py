from enum import Enum, auto
from core.ui.font import FontEngine
from helper import read_constant_from_file

class SizeBar(Enum):
    BOTTOM = auto()
    TOP = auto()

class PlayerUIManager:
    def __init__(self, window, player):
        self.location = SizeBar.BOTTOM
        self.window = window
        self.player = player
        self.bar_width = self.window.get_width()  # Start with the full window width
        self.bar_height = 20  # Default height for top/bottom bars
        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)  # Using your custom surface creation
        self.rect_position = (0, 0)
        self.font = FontEngine(30).font
        self.score_font = FontEngine(50).font
        self.last_reset_time = self.window.get_current_time()
        
    def scale(self):
        # Recalculate the position and size of the progress bar based on window resizing
        if self.location == SizeBar.BOTTOM:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, self.window.get_height() - self.bar_height)
        elif self.location == SizeBar.TOP:
            self.bar_width = self.window.get_width()
            self.rect_position = (0, 0)

        self.surface = self.window.make_surface(self.bar_width, self.bar_height, True)
        

    def toggle_location(self):
        if self.location == SizeBar.BOTTOM:
            self.location = SizeBar.TOP
        else:
            self.location = SizeBar.BOTTOM

    def reset_timer(self):
        self.last_reset_time = self.window.get_current_time()

    def draw_player_info(self):
        now = self.window.get_current_time()
        elapsed_ms = now - self.last_reset_time
        seconds = (elapsed_ms // 1000) % 60
        minutes = (elapsed_ms // 60000)

        # Prepare text
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surface = self.font.render(time_text, True, (255, 255, 255))

        size_text = f"Size: {round(self.player.diam)}"
        size_surface = self.font.render(size_text, True, (255, 255, 255))

        

        size_to_level_up_text = f"Size to level up: {self.player.level_up_size}"
        size_to_level_up_surface = self.font.render(size_to_level_up_text, True, (255,255,255))

        line_spacing = 20

        if self.location == SizeBar.TOP:
            top_y = self.bar_height

            high_score_text = f"High Score: {self.player.current_high_score}"
            high_score_surface = self.score_font.render(high_score_text, True, (255,74,128))
            high_score_surface_rect = high_score_surface.get_rect(right = self.window.get_width() - 5, top = top_y)

            score_text = f"Score: {self.player.score}"
            score_surface = self.score_font.render(score_text, True, (255,255,0))
            score_surface_rect = score_surface.get_rect(right = high_score_surface_rect.left - 10, top = top_y)

            level_text = f"Level: {self.player.current_level}"
            level_surface = self.score_font.render(level_text, True, (255,255,255))
            level_surface_rect = level_surface.get_rect(right = score_surface_rect.left - 10, top = top_y)

            self.window.blit(time_surface, (10, top_y))
            self.window.blit(size_surface, (10, top_y + line_spacing))
            self.window.blit(high_score_surface, high_score_surface_rect)
            self.window.blit(score_surface, score_surface_rect)
            self.window.blit(level_surface, level_surface_rect)
            self.window.blit(size_to_level_up_surface, (time_surface.get_rect().right + 30, top_y))

        elif self.location == SizeBar.BOTTOM:
            bottom_y = self.window.get_height() - self.bar_height - 90

            high_score_text = f"High Score: {self.player.current_high_score}"
            high_score_surface = self.score_font.render(high_score_text, True, (255,74,128))
            high_score_surface_rect = high_score_surface.get_rect(right = self.window.get_width() - 5, top = self.window.get_height() - self.bar_height - 45)

            score_text = f"Score: {self.player.score}"
            score_surface = self.score_font.render(score_text, True, (255,255,0))
            score_surface_rect = score_surface.get_rect(right = high_score_surface_rect.left - 10, top = self.window.get_height() - self.bar_height - 45)

            level_text = f"Level: {self.player.current_level}"
            level_surface = self.score_font.render(level_text, True, (255,255,255))
            level_surface_rect = level_surface.get_rect(right = score_surface_rect.left - 10, top = self.window.get_height() - self.bar_height - 45)

            self.window.blit(time_surface, (10, bottom_y + line_spacing))
            self.window.blit(size_surface, (10, bottom_y + line_spacing * 2))
            self.window.blit(size_to_level_up_surface, (10, bottom_y + line_spacing * 3))
            self.window.blit(high_score_surface, high_score_surface_rect)
            self.window.blit(score_surface, score_surface_rect)
            self.window.blit(level_surface, level_surface_rect)

    def draw(self):

        self.surface.fill((0, 0, 0))

        if self.location in [SizeBar.TOP, SizeBar.BOTTOM]:
            size_avg = self.player.diam
            progress = min(size_avg / self.player.level_up_size, 1.0)
            fill_width = int(self.bar_width * progress)
            fill_width = max(fill_width, 1)

            outline_rect = self.window.Rect(0, 0, self.bar_width, self.bar_height)

            fill_color = (
                max(0, min(255, int(255 * (1 - progress)))),
                max(0, min(255, int(255 * progress))),
                0
            )
            fill_rect = self.window.Rect(
                outline_rect.left + 2,       
                outline_rect.top + 2,        
                fill_width - 4,
                self.bar_height - 4
            )

            self.window.draw_rect(self.surface, fill_color, fill_rect)
            self.window.draw_rect(self.surface, (255, 255, 255), outline_rect, 2)
            
        

        self.window.blit(self.surface, self.rect_position)
        self.draw_player_info()

    def update(self):
        self.scale()