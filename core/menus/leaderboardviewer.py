import threading

from systemlogging import log_event, log_error

from core.application.network.leaderboard import Leaderboard
from core.loading.LoadingScreenManager import LoadingScreenManager
from core.state.RuntimeLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.RuntimeLayer.NetworkLayer.Loading.statemanager import FetchStateManager
from core.ui.font import FontEngine
from core.ui.scrollabletext import ScrollableText


class LeaderboardViewer:

    USERNAME_X = 0.20
    SCORE_X = 0.65
    HEADER_Y = 0.30
    BODY_Y = 0.40


    def __init__(self, system):

        self.system = system

        self.loading = LoadingScreenManager(system)
        self.leaderboard = Leaderboard(system)

        self.font = FontEngine(50).font

        self.fetch_manager = FetchStateManager()

        self.cached_data = None
        self.fetch_thread = None

        self.lock = threading.Lock()

        self.last_display_data = None


        self.leaderboard_text = ScrollableText(
            system,
            font_size=50,
            anchor=(
                self.USERNAME_X,
                self.BODY_Y
            ),
            width=0.65,
            height=0.50,
            align="left",
            line_spacing=0.015
        )


        self.timeout_text = ScrollableText(
            system,
            font_size=50,
            anchor=(0.5,0.5),
            width=0.8,
            height=0.2,
            align="center"
        )


    def start_fetch(self):

        if not self.fetch_manager.is_state(FETCH_STATE.IDLE):
            return

        self.fetch_thread = threading.Thread(
            target=self.fetch_task,
            daemon=True
        )

        self.fetch_thread.start()


    def fetch_task(self):

        self.fetch_manager.set_state(
            FETCH_STATE.FETCHING
        )

        try:

            status, data = (
                self.leaderboard.fetch_leaderboard()
            )

        except Exception as e:

            log_event(
                "Leaderboard fetch exception",
                str(e)
            )

            with self.lock:

                self.cached_data = None

                self.fetch_manager.set_state(
                    FETCH_STATE.ERROR
                )

            return


        with self.lock:

            if status == "success":

                self.cached_data = data

                self.fetch_manager.set_state(
                    FETCH_STATE.SUCCESS
                )

            elif status == "timeout":

                self.cached_data = None

                self.fetch_manager.set_state(
                    FETCH_STATE.TIMEOUT
                )

            else:

                self.cached_data = None

                self.fetch_manager.set_state(
                    FETCH_STATE.ERROR
                )


    def fetch_and_display(self):

        if self.cached_data is None:

            if self.fetch_manager.is_state(FETCH_STATE.IDLE):

                self.start_fetch()


            elif self.fetch_manager.is_state(FETCH_STATE.FETCHING):

                self.loading.draw(
                    "Fetching leaderboard data..."
                )


            elif self.fetch_manager.is_state(FETCH_STATE.TIMEOUT):

                self.display_timeout()


            elif self.fetch_manager.is_state(FETCH_STATE.ERROR):

                log_error(
                    "Error fetching leaderboard data."
                )

                self.fetch_manager.set_state(
                    FETCH_STATE.IDLE
                )

            return


        self.display_leaderboard(
            self.cached_data
        )


    def display_timeout(self):

        self.timeout_text.set_text(
                [
                    (
                        "Leaderboard Timed Out. Please try again later.",
                        0.5,
                        (255,0,0)
                    )
                ]
        )

        self.timeout_text.draw()


    def draw_header(self):

        username = self.font.render(
            "USERNAME",
            True,
            (255,255,0)
        )

        score = self.font.render(
            "SCORE",
            True,
            (255,255,0)
        )


        ux, uy = self.leaderboard_text.normalized_to_pixel(
            self.USERNAME_X,
            self.HEADER_Y
        )

        sx, sy = self.leaderboard_text.normalized_to_pixel(
            self.SCORE_X,
            self.HEADER_Y
        )


        self.system.window.blit(
            username,
            username.get_rect(
                left=ux,
                centery=uy
            )
        )


        self.system.window.blit(
            score,
            score.get_rect(
                left=sx,
                centery=sy
            )
        )


    def display_leaderboard(self, data):

        if data != self.last_display_data:

            self.last_display_data = data

            sorted_data = sorted(data, key=lambda entry: entry["score"], reverse=True)

            lines = []

            for index, entry in enumerate(sorted_data):

                username = entry["username"]
                score = entry["score"]

                t = self.system.time.get_current_time() / 100
                pulse = (self.system.math.sin(t) + 1) / 2

                if username == self.system.user.username:

                    color = lambda: (
                        int(20 + 180 * ((self.system.math.sin(self.system.time.get_current_time() / 100) + 1) / 2)),
                        255,
                        int(20 + 180 * ((self.system.math.sin(self.system.time.get_current_time() / 100) + 1) / 2))
                    )

                else:

                    color = (255, 255, 255)

                lines.append([
                    (f"{index + 1}. {username}", self.USERNAME_X, color),
                    (str(score), self.SCORE_X, color)
                ])

            self.leaderboard_text.set_text(lines)

        self.draw_header()
        self.leaderboard_text.draw()


    def scroll(self, amount):
        self.leaderboard_text.scroll(amount)

    def refresh(self):
        self.cached_data = None
        self.last_display_data = None
        self.leaderboard_text.set_text([])
        self.fetch_manager.set_state(FETCH_STATE.IDLE)
        self.start_fetch()


    def handle_event(self, event):
        if event.type == self.system.input.mouse_scroll_event():
            self.scroll(-event.y)