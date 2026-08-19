from core.state.RuntimeLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.RuntimeLayer.Audio.Music.state import MUSIC_STATE
from core.state.RuntimeLayer.Audio.Application.state import APP_SFX_STATE
from core.state.RuntimeLayer.NetworkLayer.Login.state import LOGIN_STATE

from core.state.ApplicationLayer.Game.state import GAMESTATE

from core.application.network.leaderboard import Leaderboard

class UI_Utility:
    def __init__(self,dr):
        self.distant_realms = dr
        self.system = dr.system

    def update_audio(self):
        if (self.distant_realms.ui_controller.active_name == "audio_settings"
            or self.distant_realms.ui_controller.active_name == "pause_audio_settings"):

            music_vol = float(self.distant_realms.system.sound.volume)
            normal_mvol = str(int(music_vol * 10))

            sfx_vol = float(self.distant_realms.system.sound.sfx_volume)
            normal_sfxvol = str(int(sfx_vol * 10))

            for child in self.get_elements():
                if child.id == "music_volumeV":
                    child.text = normal_mvol
                
                elif child.id == "sfx_volumeV":
                    child.text = normal_sfxvol

                elif child.id == "music_state":
                    if self.system.sound.music_state.is_state(MUSIC_STATE.ON):
                        child.text = "ON"
                    elif self.system.sound.music_state.is_state(MUSIC_STATE.OFF):
                        child.text = "OFF"
                    else:
                        child.text = "None"

                elif child.id == "ui_sfx_state":
                    if self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                        child.text = "ON"
                    elif self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.OFF):
                        child.text = "OFF"
                    else:
                        child.text = "None"

                elif child.id == "game_sfx_state":
                    if self.system.sound.app_sfx_state.is_state(APP_SFX_STATE.ON):
                        child.text = "ON"
                    elif self.system.sound.app_sfx_state.is_state(APP_SFX_STATE.OFF):
                        child.text = "OFF"
                    else:
                        child.text = "None"

    def display_username(self):
        if (self.distant_realms.ui_controller.active_name == "main_menu"
            or self.distant_realms.ui_controller.active_name == "update_available_menu" 
            ):
            username = str(self.distant_realms.application.user.username)

            for child in self.get_elements():
                if child.id == "username_greet":
                    child.text = username

    def display_score(self):
            if (self.distant_realms.ui_controller.active_name == "main_menu"
                or self.distant_realms.ui_controller.active_name == "update_available_menu" 
                ):
                score = str(self.distant_realms.application.user.high_score)
                if score:    
                    for child in self.get_elements():
                        if child.id == "score_value":
                            child.text = score

    def display_login_suggestion(self):
        if (self.distant_realms.ui_controller.active_name == "main_menu"
            or self.distant_realms.ui_controller.active_name == "update_available_menu" 
            ):
            
            for child in self.get_elements():
                if child.id == "login_suggestion":

                    if self.distant_realms.system.login_state.is_state(LOGIN_STATE.LOGGED_IN):
                        child.text = ""

    def get_elements(self):
        return self.distant_realms.ui_controller.get_active_ui().children

    def toggle_music(self):
        
        if self.distant_realms.application.snow_blitz.state:
            if not self.distant_realms.application.snow_blitz.state.is_state(GAMESTATE.NONE):
                self.system.sound.toggle_music()
        else:
            self.system.sound.toggle_music("LoFiSi")

    def toggle_ui_sfx(self):
        if self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
            self.system.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.OFF)
        elif self.system.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.OFF):
            self.system.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.ON)

    def toggle_game_sfx(self):
        if self.system.sound.app_sfx_state.is_state(APP_SFX_STATE.ON):
            self.system.sound.app_sfx_state.set_state(APP_SFX_STATE.OFF)
        elif self.system.sound.app_sfx_state.is_state(APP_SFX_STATE.OFF):
            self.system.sound.app_sfx_state.set_state(APP_SFX_STATE.ON)