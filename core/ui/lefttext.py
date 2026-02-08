from core.ui.font import FontEngine

class LeftAlignedText:
    def __init__(self, board_surface):
        self.font = FontEngine(40).font
        self.board_surface = board_surface

    def _draw_left_aligned_text(self, text):
        lines = text.split("\n")
        surface_height = self.board_surface.get_height()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        margin_left = 50

        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 255))
            rect = surf.get_rect(topleft=(margin_left, start_y + i * self.font.get_height() * 1.1))
            self.board_surface.blit(surf, rect)
