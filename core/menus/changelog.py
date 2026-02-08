from core.ui.lefttext import LeftAlignedText
from config import config

class ChangeLog(LeftAlignedText):
    def __init__(self, board_surface):
        super().__init__(board_surface)
        self.changelog_text = []
        self.load_changelog_from_file("changelog.txt")  # Ensure the changelog is loaded on init

    def load_changelog_from_file(self, file_path):
        try:
            with open(file_path, "r") as f:
                self.changelog_text = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("Changelog file not found, using default empty changelog.")

    def clear_changelog_file(self):
        try:
            with open("changelog.txt", "w") as f:
                f.write("")
            print("Changelog file cleared.")
        except Exception as e:
            print(f"Error clearing changelog file: {e}")

    def draw(self):

        if not self.changelog_text:
            self._draw_left_aligned_text("No changelog available.")
            return

        changelog_content = "\n".join(self.changelog_text)
        
        self._draw_left_aligned_text(changelog_content)

    def rescale(self):
        self.draw()
