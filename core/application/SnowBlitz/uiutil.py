class UI_Utility:
    def __init__(self,dr):
        self.distant_realms = dr

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
                
                if child.id == "sfx_volumeV":
                    child.text = normal_sfxvol

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

    def get_elements(self):
        return self.distant_realms.ui_controller.get_active_ui().children