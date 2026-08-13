
class ActionRegistrar:
    def __init__(self, distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system
        
    def register(self):
        application = self.distant_realms

        
        # application functions
        application.actions.register("resume_game", lambda: application.application.snow_blitz.toggle_pause())
        application.actions.register("reset_game", lambda: application.application.navigation.reset_simulation())

        # game menu functions
        application.actions.register("game_main_menu", lambda: application.application.navigation.game_main_menu())
        application.actions.register("open_game_settings", lambda: application.application.navigation.open_pause_settings())
        application.actions.register("back_to_pause_root", lambda: application.application.navigation.back_to_pause_root())
        application.actions.register("open_sb_settings", lambda: application.application.navigation.open_sb_settings())
        application.actions.register("toggle_progress_bar", lambda: application.application.snow_blitz.hud.toggle())
        application.actions.register("pause_open_audio", lambda: application.application.navigation.audio_settings())

        # main menu functions
        application.actions.register("start_endless_mode", lambda: application.application.navigation.start_endless_mode())
        application.actions.register("start_tutorial_mode", lambda: application.application.navigation.start_tutorial_mode())
        application.actions.register("open_changelog",lambda: application.ui_controller.show_ui("changelog"))
        application.actions.register("open_credits",lambda: application.ui_controller.show_ui("credits"))
        application.actions.register("view_leaderboard", lambda: application.application.load_leaderboard())
        application.actions.register("app_main_menu", lambda: application.application.navigation.app_main_menu())

        # settings menu functions
        application.actions.register("open_settings",lambda: application.ui_controller.show_ui("settings_root"))
        application.actions.register("audio_settings",lambda: application.ui_controller.show_ui("audio_settings"))

        # system functions
        application.actions.register("mvolup", self.system.sound.volume_up)
        application.actions.register("mvoldown", self.system.sound.volume_down)
        application.actions.register("sfxvolup", self.system.sound.sfx_volume_up)
        application.actions.register("sfxvoldown", self.system.sound.sfx_volume_down)
        application.actions.register("quit",self.system.quit)