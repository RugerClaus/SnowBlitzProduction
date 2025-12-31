from core.ui.font import FontEngine
from config import config

class Credits:
    def __init__(self,board_surface):
        self.font = FontEngine(60).font
        self.board_surface = board_surface
        self.authors = config["AUTHORS"]

    def draw(self):
        title = config["TITLE"]
        soundtrack = f"Soundtrack by {self.authors[0]}"
        design = f"Designed on the Distant Realms Python framework by {self.authors[0]}"
        logo = f"Logo by {self.authors[1]}"
        self._draw_centered_text(f"{title}\n{soundtrack}\n{design}\n{logo}\n")
    
    def rescale(self):
        self.draw()


    def _draw_centered_text(self, text):
        lines = text.split("\n")
        surface_height = self.board_surface.get_height()
        surface_width = self.board_surface.get_width()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 255))
            rect = surf.get_rect(center=(surface_width // 2,
                                         start_y + i * self.font.get_height() * 2))
            self.board_surface.blit(surf, rect)
