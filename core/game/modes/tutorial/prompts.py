from core.ui.font import FontEngine

class Prompts:
    def __init__(self, board_surface, player, input):
        self.board_surface = board_surface
        self.player = player
        self.input = input
        self.font = FontEngine(55).font

        self.player_has_moved = False
        self.player_has_continued = False

    def movement_prompt(self):
        if not self.player_has_moved:
            self._draw_centered_text(f"Press {self.input.get_current_left_control()} or {self.input.get_current_right_control()} to move")

    def snow_prompt(self):
        if not self.player_has_continued:
            self._draw_centered_text(
                "Collide with snowflakes to grow\nPress SPACE to continue"
            )

    def rock_prompt(self):
        if not self.player_has_continued:
            self._draw_centered_text(
                "Rocks are dangerous! Avoid them\nPress SPACE to continue"
            )

    def powerup_prompt(self):
        if not self.player_has_continued:
            self._draw_centered_text(
                "Powerups:\nBlue: Absorb Rock\nGreen: Stop Shrinking\nPress SPACE to continue"
            )

    def reducer_prompt(self):
        if not self.player_has_continued:
            self._draw_centered_text(
                "Level Reducers lower your level-up size\nPress SPACE to continue"
            )

    def end_prompt(self):
        if not self.player_has_continued:
            self._draw_centered_text("Tutorial Complete!\nPress SPACE to go to the main menu")

    def handle_movement_input(self, controls):
        keys = self.input.get_pressed_keys()
        if keys[controls.move_left] or keys[controls.move_right]:
            self.player_has_moved = True

    def handle_continue_input(self):
        keys = self.input.get_pressed_keys()
        if keys[self.input.keys.space_key()]:
            self.player_has_continued = True

    def _draw_centered_text(self, text):
        lines = text.split("\n")
        surface_height = self.board_surface.get_height()
        surface_width = self.board_surface.get_width()

        total_height = len(lines) * self.font.get_height() * 1.2
        start_y = surface_height // 2 - total_height // 2

        for i, line in enumerate(lines):
            surf = self.font.render(line, True, (255, 255, 128))
            rect = surf.get_rect(center=(surface_width // 2,
                                         start_y + i * self.font.get_height() * 1.2))
            self.board_surface.blit(surf, rect)
