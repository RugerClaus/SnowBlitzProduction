from core.menus.basemenu import BaseMenu
from core.ui.button import Button
from core.ui.newbutton import Button as newb
from core.state.RuntimeLayer.Menu.Pause.state import PAUSE_MENU_STATE
from core.state.RuntimeLayer.Menu.Pause.statemanager import PauseMenuStateManager
from core.application.entities.player.ui.uimanager import SizeBar
from core.state.ApplicationLayer.state import GAMESTATE

class Pause(BaseMenu):
    def __init__(self, system, game, resume_callback, reset_game_callback):
        self.system = system
        self.game = game
        super().__init__(system)
        self.resume_callback = resume_callback
        self.reset_game_callback = reset_game_callback
        self.state = PauseMenuStateManager()
        
        self.menu_config = {
            "Root": [
                ("Resume", self.resume_callback, 0.30),
                ("Main Menu", self.system.go_to_menu, 0.40),
                ("Reset Game", self.reset_game_callback, 0.50),
                ("Settings", self.go_to_settings, 0.60),
                ("Quit", self.system.quit, 0.70),
            ],

            "Settings": [
                ("Audio", self.audio_settings, 0.45),
                ("Progress Bar", None, 0.55),
                ("Back", self.back_to_root, 0.65),
            ],

            "Audio": [
                ("-", self.system.sound.volume_down, 0.35, 0.40),
                (f"Music Vol: {int(self.system.sound.volume * 10)}", None, 0.50, 0.40),
                ("+", self.system.sound.volume_up, 0.65, 0.40),

                ("-", self.system.sound.sfx_volume_down, 0.35, 0.50),
                (f"SFX Vol: {int(self.system.sound.sfx_volume * 10)}", None, 0.50, 0.50),
                ("+", self.system.sound.sfx_volume_up, 0.65, 0.50),

                ("Music:", self.system.sound.toggle_music, 0.50, 0.60),
                ("UI SFX:", self.toggle_ui_sfx, 0.50, 0.70),
                ("Game SFX:", self.toggle_game_sfx, 0.50, 0.80),
                ("Back", self.go_to_settings, 0.50, 0.90),
            ]
        }
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []

        if self.state.is_state(PAUSE_MENU_STATE.ROOT):
            for text, callback, y in self.menu_config["Root"]:
                self.buttons.append(
                    newb(
                        self.system,
                        40,
                        text,
                        (0.5, y),
                        callback
                    )
                )

        elif self.state.is_state(PAUSE_MENU_STATE.SETTINGS):
            for text, callback, y in self.menu_config["Settings"]:
                self.buttons.append(
                    newb(
                        self.system,
                        40,
                        text,
                        (0.5, y),
                        callback
                    )
                )

        elif self.state.is_state(PAUSE_MENU_STATE.AUDIO):
            for text, callback, x, y in self.menu_config["Audio"]:
                self.buttons.append(
                    newb(
                        self.system,
                        35 if text in ("+", "-") else 40,
                        text,
                        (x, y),
                        callback
                    )
                )

    def update_toggle_game_buttons(self):
        for button in self.buttons:
            if button.text.startswith("Progress Bar:"):
                button.set_new_text(f"Progress Bar: {'Top' if self.game.progress_bar.location == SizeBar.TOP else 'Bottom'}")

    def update(self):
        self.update_toggle_buttons()
        self.update_toggle_game_buttons()
        if self.game.game_state.is_state(GAMESTATE.PLAYING):
            self.back_to_root()

    def reset_menu(self):
        self.state.set_state(PAUSE_MENU_STATE.ROOT)
        self.create_buttons()

    def audio_settings(self):
        self.state.set_state(PAUSE_MENU_STATE.AUDIO)
        self.create_buttons()

    def back_to_root(self):
        self.state.set_state(PAUSE_MENU_STATE.ROOT)
        self.create_buttons()

    def go_to_settings(self):
        self.state.set_state(PAUSE_MENU_STATE.SETTINGS)
        self.create_buttons()

    def on_resize(self):
        self.create_buttons()

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
                

        elif event.type == self.system.input.video_resize_event():
            self.on_resize()

    def draw(self):

        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw()

        self.set_title("PAUSED")

        if self.state.is_state(PAUSE_MENU_STATE.SETTINGS):
            self.set_title("SETTINGS")

        if self.state.is_state(PAUSE_MENU_STATE.AUDIO):
            self.set_title("AUDIO SETTINGS")

        self.draw_title()