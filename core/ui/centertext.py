from core.ui.font import FontEngine
from config import config

class CenterText:
    def __init__(self,board_surface):
        self.font = FontEngine(40).font
        self.board_surface = board_surface

    def _draw_centered_text(self, text):
        lines = text.split("\n")
        surface_height = self.board_surface.get_height()
        surface_width = self.board_surface.get_width()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 255))
            rect = surf.get_rect(center=(surface_width // 2,
                                         start_y + i * self.font.get_height() * 1.1))
            self.board_surface.blit(surf, rect)
