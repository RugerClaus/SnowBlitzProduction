import threading
from helper import *
from core.ui.font import FontEngine
from core.network.leaderboard import Leaderboard

class LeaderboardViewer():
    def __init__(self,window,sound,state,input,root_callback):
        self.window = window
        self.sound = sound
        self.state = state
        self.input = input
        self.root_callback = root_callback
        self.leaderboard = Leaderboard()
        self.font = FontEngine(50).font
        
        self.loading = False
        self.cached_data = None
        self.fetch_thread = None

    def start_fetch(self):
        if self.fetch_thread and self.fetch_thread.is_alive():
            return

        self.loading = True
        self.fetch_thread = threading.Thread(target=self._fetch_task, daemon=True)
        self.fetch_thread.start()

    def _fetch_task(self):
        status, data = self.leaderboard.fetch_leaderboard()
        self.loading = False

        if status == "success" and data:
            self.cached_data = data
        else:
            self.cached_data = None
            self.fetch_status = status

    def fetch_and_display(self):
        if self.cached_data is None:
            if not self.loading:
                self.start_fetch()
            if hasattr(self, "fetch_status") and self.fetch_status == "timeout":
                self.display_timeout()
            else: 
                draw_loading(self.font, self.window, "Loading Leaderboard...")

            return

        self.display_leaderboard(self.cached_data)


    def display_timeout(self):
        text = self.font.render("Leaderboard Timed Out. Please try again later.", True, (255, 0, 0))
        rect = text.get_rect(center=(self.window.get_screen().get_width() // 2, self.window.get_screen().get_height() // 2))
        self.window.blit(text, rect)

    def display_leaderboard(self, data):
        center_x = self.window.get_width() // 2
        start_y = self.window.get_height() // 3
        row_height = 60
        column_gap = 300

        username_x = center_x - column_gap // 2
        score_x = center_x + column_gap // 2

        header_color = (255, 255, 0)
        text_color = (255, 255, 255)

        username_header = self.font.render("Username", True, header_color)
        score_header = self.font.render("Score", True, header_color)

        self.window.blit(username_header, username_header.get_rect(center=(username_x, start_y)))
        self.window.blit(score_header, score_header.get_rect(center=(score_x, start_y)))

        sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]

        for row, entry in enumerate(sorted_data):
            y = start_y + (row + 1) * row_height

            username_surf = self.font.render(entry["username"], True, text_color)
            score_surf = self.font.render(str(entry["score"]), True, text_color)

            self.window.blit(username_surf, username_surf.get_rect(center=(username_x, y)))
            self.window.blit(score_surf, score_surf.get_rect(center=(score_x, y)))

        log_event("Displaying leaderboard data.", f"{self.leaderboard}")

    def refresh(self):
        self.cached_data = None
        self.fetch_status = None
        self.start_fetch()
