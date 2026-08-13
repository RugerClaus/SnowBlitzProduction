import threading

from systemlogging import log_event, log_error

from core.application.network.leaderboard import Leaderboard
from core.loading.LoadingScreenManager import LoadingScreenManager
from core.state.RuntimeLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.RuntimeLayer.NetworkLayer.Loading.statemanager import FetchStateManager
from core.ui.font import FontEngine
from core.ui.widgets.scrollabletext import ScrollableText


class LeaderboardViewer:

    # Coordinates INSIDE the ScrollableText widget.
    USERNAME_X = 0.05
    SCORE_X = 0.70

    # Widget geometry.
    BODY_POSITION = (0.50, 0.45)
    BODY_WIDTH = 0.65
    BODY_HEIGHT = 0.50

    HEADER_OFFSET = 0.035

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
            id="leaderboard_text",
            font_size=50,
            position=self.BODY_POSITION,
            width=self.BODY_WIDTH,
            height=self.BODY_HEIGHT,
            align="left",
            line_spacing=0.015
        )

        self.timeout_text = ScrollableText(
            system,
            id="leaderboard_timeout",
            font_size=50,
            position=(0.5, 0.5),
            width=0.8,
            height=0.2,
            align="center"
        )

    # ---------------------------------------------------------
    # Fetch
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    def draw_header(self):

        widget = self.leaderboard_text

        username = self.font.render(
            "USERNAME",
            True,
            (255, 255, 0)
        )

        score = self.font.render(
            "SCORE",
            True,
            (255, 255, 0)
        )

        # The ScrollableText surface is centered at widget.rect.center.
        #
        # Convert the widget-local X positions into screen coordinates.

        username_x = (
            widget.rect.left
            + int(
                widget.surface.get_width()
                * self.USERNAME_X
            )
        )

        score_x = (
            widget.rect.left
            + int(
                widget.surface.get_width()
                * self.SCORE_X
            )
        )
        
        header_y = (
            widget.rect.top
            - int(
                self.system.window.get_height()
                * self.HEADER_OFFSET
            )
        )

        self.system.window.blit(
            username,
            username.get_rect(
                left=username_x,
                centery=header_y
            )
        )

        self.system.window.blit(
            score,
            score.get_rect(
                left=score_x,
                centery=header_y
            )
        )

    def display_leaderboard(self, data):

        if data != self.last_display_data:

            self.last_display_data = data

            sorted_data = sorted(
                data,
                key=lambda entry: entry["score"],
                reverse=True
            )

            lines = []

            for index, entry in enumerate(sorted_data):

                username = entry["username"]
                score = entry["score"]

                if username == self.system.user.username:

                    color = lambda: (
                        int(
                            20
                            + 180
                            * (
                                (
                                    self.system.math.sin(
                                        self.system.time.get_current_time()
                                        / 100
                                    )
                                    + 1
                                )
                                / 2
                            )
                        ),
                        255,
                        int(
                            20
                            + 180
                            * (
                                (
                                    self.system.math.sin(
                                        self.system.time.get_current_time()
                                        / 100
                                    )
                                    + 1
                                )
                                / 2
                            )
                        )
                    )

                else:

                    color = (255, 255, 255)

                lines.append([
                    (
                        f"{index + 1}. {username}",
                        self.USERNAME_X,
                        color
                    ),
                    (
                        str(score),
                        self.SCORE_X,
                        color
                    )
                ])

            self.leaderboard_text.set_text(
                lines
            )

        self.draw_header()
        self.leaderboard_text.draw()

    def display_timeout(self):

        self.timeout_text.set_text([
            [
                (
                    "Leaderboard Timed Out. Please try again later.",
                    0.5,
                    (255, 0, 0)
                )
            ]
        ])

        self.timeout_text.draw()

    def handle_event(self, event):

        self.leaderboard_text.handle_event(event)
        self.timeout_text.handle_event(event)

    def scroll(self, amount):

        self.leaderboard_text.scroll(amount)

    def refresh(self):

        self.cached_data = None
        self.last_display_data = None

        self.leaderboard_text.set_text([])

        self.fetch_manager.set_state(
            FETCH_STATE.IDLE
        )

        self.start_fetch()