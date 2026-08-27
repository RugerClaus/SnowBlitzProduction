from helper import sine

from core.loading.LoadingScreenManager import LoadingScreenManager

from core.ui.type import COMPOSABLE

from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

from application.network.sessions import Session
from application.network.authentication import Authentication
from core.engine.user import User
from application.SnowBlitz.navigation import Navigation
from application.SnowBlitz.debug.uiutil import UI_Utility
from application.SnowBlitz.debug.genutil import Gen_Utility
from application.auth import Auth

class Application:
    def __init__(self,distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system
        
        self.session = Session(self.system)
        self.session_started = False 

        self.leaderboard = None

        self.snow_blitz = None

        self.auth = Authentication(self)
        self.formauth = Auth(self)

        self.user = User(self.system)
        if self.user.username:
            self.auth.auto_login()

        self.navigation = Navigation(self)
        self.gen_util = Gen_Utility(self.distant_realms)
        self.ui_util = UI_Utility(self.distant_realms)

        self.clean_up_states()

        self.init_main()

        self.loading_screen = LoadingScreenManager(self.system)

        self.loading_start = None
        self.loading_thread = None
        self.loading_error = None

        self.simulation_ready = False

    def init_main(self):
        self.navigation.app_main_menu()
    
    def handle_event(self, event, command=None):
        if not self.snow_blitz:
            if not self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.session_started = False

        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.handle_event(event, command)

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.gen_util.handle_event(event, command)

        activeui = self.distant_realms.ui_controller.get_active_ui()
        if activeui:
            if activeui.type == COMPOSABLE.FORM:
                self.formauth.handle_event(event, command)

        
    def update(self):

        self.ui_util.update_audio()

        pulse = sine(self.system.time.get_current_time())
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)
        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.update()
        else:
            self.ui_util.display_username()
            self.ui_util.display_score()
            self.ui_util.display_login_suggestion()

        activeui = self.distant_realms.ui_controller.get_active_ui()
        if activeui:
            if activeui.type == COMPOSABLE.FORM:
                self.formauth.update()
        

    def draw(self):
        if self.loading_thread is not None and not self.simulation_ready:
            if self.loading_error is not None:
                self.loading_screen.draw(f"Loading failed: {self.loading_error}")
            else:
                elapsed = self.system.time.performance_time()- self.loading_start
                self.loading_screen.draw(f"Loading world... {elapsed:.2f}s")
            return

        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.draw()

        if self.leaderboard:
            self.leaderboard.fetch_and_display()

            
    def scale(self):
        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.scale()
        if self.leaderboard:
            self.load_leaderboard()

    def register_debug_telemetry(self):
        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.register_debug_telemetry()
            
    def reset(self):
        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.reset()
            self.snow_blitz.reset_systems()


    def clean_up_states(self):
        self.system.app_inspector.clear()
        if self.snow_blitz and self.simulation_ready:
            self.snow_blitz.clean_up_states()
        self.session.clean_up_states()

    def load_leaderboard(self):
        import importlib
        from application.SnowBlitz import leaderboardviewer

        importlib.reload(leaderboardviewer)

        self.leaderboard = leaderboardviewer.LeaderboardViewer(self.system)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("leaderboard")

    def load_snow_blitz(self):
        import importlib
        from application.SnowBlitz import snowblitz
        importlib.reload(snowblitz)

        self.snow_blitz = snowblitz.SnowBlitz(self)
        self.distant_realms.ui_controller.clear()

    def load_simulation_task(self, game_mode):

        try:

            self.load_snow_blitz()

            self.snow_blitz.load_world()

            self.snow_blitz.init_game(game_mode)

            self.simulation_ready = True

        except Exception as e:

            self.loading_error = e

            print(
                "Game loading failed:",
                e
            )