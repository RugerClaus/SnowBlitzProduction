import threading
from core.util.colors import *

from core.state.RuntimeLayer.NetworkLayer.Update.state import UPDATE_STATE
from core.state.ApplicationLayer.GameMode.state import GAME_MODE
from core.state.ApplicationLayer.Game.state import GAMESTATE
from core.state.RuntimeLayer.NetworkLayer.Login.state import LOGIN_STATE
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE
from core.state.RuntimeLayer.Audio.Music.state import MUSIC_STATE

class Navigation:

    def __init__(self,application):
        self.application = application

    def start_endless_mode(self):
        self.application.distant_realms.ui_controller.clear()
        if self.application.system.sound.music_state.is_state(MUSIC_STATE.ON):
            self.application.system.sound.play_music()
        self.application.session_started = False
        self.application.simulation_ready = False
        self.application.loading_error = None
        self.application.loading_start = (self.application.system.time.performance_time())
        self.application.loading_thread = threading.Thread(target=self.application.load_simulation_task,args=('endless',),daemon=True)
        self.application.loading_thread.start()


    def start_tutorial_mode(self):
        self.application.distant_realms.ui_controller.clear()
        if self.application.system.sound.music_state.is_state(MUSIC_STATE.ON):
            self.application.system.sound.play_music()
        self.application.session_started = False
        self.application.simulation_ready = False
        self.application.loading_error = None
        self.application.loading_start = self.application.system.time.performance_time()
        self.application.loading_thread = threading.Thread(target=self.application.load_simulation_task,args=("tutorial",),daemon=True)
        self.application.loading_thread.start()


    def reset_simulation(self):
        self.application.gen_util.lb.get_logged_in_user_score()
        if self.application.snow_blitz.mode.is_state(GAME_MODE.ENDLESS):
            self.start_endless_mode()

        elif self.application.snow_blitz.mode.is_state(GAME_MODE.TUTORIAL):
            self.start_tutorial_mode()

    def game_main_menu(self):
        self.application.gen_util.lb.get_logged_in_user_score()
        if self.application.snow_blitz:
            self.application.clean_up_states()
            self.application.snow_blitz.state.set_state(GAMESTATE.NONE)
            self.application.snow_blitz = None
        self.app_main_menu()

    def app_main_menu(self):
        if self.application.leaderboard:
            self.application.leaderboard = None
        if self.application.session.state.is_state(ONLINE_SESSION_STATE.ACTIVE):
            self.application.session.end_online_session()
        if self.application.system.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.application.distant_realms.ui_controller.show_ui("main_menu")
        elif self.application.system.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.application.distant_realms.ui_controller.show_ui("update_available_menu")

        if self.application.system.sound.music_state.is_state(MUSIC_STATE.ON):
            if not self.application.system.sound.current_track == "LoFiSi - JumpyJuggernaut.mp3":
                self.application.system.sound.play_music("LoFiSi")

    def open_pause_settings(self):
        self.application.distant_realms.ui_controller.show_ui("pause_settings")

    def back_to_pause_root(self):
        self.application.distant_realms.ui_controller.show_ui("pause")

    def open_sb_settings(self):
        self.application.distant_realms.ui_controller.show_ui("game_settings")

    def audio_settings(self):
        self.application.distant_realms.ui_controller.show_ui("pause_audio_settings")

    def log_out_user(self):
        self.application.auth.log_out()
        self.app_main_menu()

    def open_app_settings(self):
        if self.application.system.login_state.is_state(LOGIN_STATE.LOGGED_IN):
            self.application.distant_realms.ui_controller.show_ui("settings_root")
        elif self.application.system.login_state.is_state(LOGIN_STATE.LOGGED_OUT):
            self.application.distant_realms.ui_controller.show_ui("logged_out_settings_root")