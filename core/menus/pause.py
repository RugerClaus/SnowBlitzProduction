import math
from core.menus.basemenu import BaseMenu
from core.ui.button import Button
from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.Audio.Game.state import GAME_SFX_STATE
from core.state.ApplicationLayer.Menu.Pause.state import PAUSE_MENU_STATE
from core.state.ApplicationLayer.Menu.Pause.statemanager import PauseMenuStateManager
from core.game.entities.player.ui.uimanager import SizeBar
from core.state.GameLayer.state import GAMESTATE

class Pause(BaseMenu):
    def __init__(self, window, game, sound, input, resume_callback, menu_callback, quit_callback, reset_game_callback):
        self.window = window
        self.sound = sound
        self.input = input
        self.game = game
        super().__init__(window, sound)
        self.resume_callback = resume_callback
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.reset_game_callback = reset_game_callback
        self.state = PauseMenuStateManager()
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.window.get_screen().get_size()
        btn_width, btn_height = screen_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7
        center_x = screen_w // 2

        if self.state.is_state(PAUSE_MENU_STATE.ROOT):
            self.buttons = [
                Button(self.sound, self.window, "Resume", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.resume_callback),
                Button(self.sound, self.window, "Main Menu", center_x, start_y + spacing * 1, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.menu_callback),
                Button(self.sound, self.window, "Reset Game", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.reset_game_callback),
                Button(self.sound, self.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.go_to_settings),
                Button(self.sound, self.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.quit_callback),
            ]
        elif self.state.is_state(PAUSE_MENU_STATE.SETTINGS):
            self.buttons = [
                Button(self.sound, self.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.audio_settings),
                Button(self.sound, self.window, f"Progress Bar: ", center_x, start_y + spacing * 1, btn_width * 1.9, btn_height, (255, 255, 255), (128, 0, 200), self.game.progress_bar.toggle_location),
                Button(self.sound, self.window, "Back", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.back_to_root),
            ]

        elif self.state.is_state(PAUSE_MENU_STATE.AUDIO):
            self.buttons = [
                Button(self.sound, self.window, f"-", center_x - 200, self.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_down),
                Button(self.sound, self.window, f"Music Vol: {int(self.sound.volume*10)}", center_x, self.window.get_height() // 2 - spacing, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.sound, self.window, f"+", center_x + 200, self.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_up),
                
                Button(self.sound, self.window, f"-", center_x - 200, self.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.sfx_volume_down),
                Button(self.sound, self.window, f"SFX Vol: {int(self.sound.sfx_volume*10)}", center_x, self.window.get_height() // 2 + spacing * 0.01, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.sound, self.window, f"+", center_x + 200, self.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.sfx_volume_up),
                
                Button(self.sound, self.window, f"Music:", center_x, self.window.get_height() // 2 + spacing * 1, 240, btn_height,
                    (255, 255, 255), (128, 0, 200), self.sound.toggle_music),
                Button(self.sound, self.window, f"UI SFX:", center_x, self.window.get_height() // 2 + spacing * 2, 240, btn_height,
                    (255, 255, 255), (128, 0, 200), self.toggle_ui_sfx),
                Button(self.sound, self.window, f"Game SFX:", center_x, self.window.get_height() // 2 + spacing * 3, 340, btn_height,
                    (255, 255, 255), (128, 0, 200), self.toggle_game_sfx),
                Button(self.sound, self.window, "Back", center_x, self.window.get_height() // 2 + spacing * 4, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.go_to_settings)
            ]

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
        if event.type == self.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
                

        elif event.type == self.input.video_resize_event():
            self.on_resize()

    def draw(self):
        t = self.window.get_current_time() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            0,
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.window.fill(fade_color)

        mouse_pos = self.input.get_mouse_pos()
        for button in self.buttons:
            button.draw(mouse_pos)

        self.set_title("PAUSED")

        if self.state.is_state(PAUSE_MENU_STATE.SETTINGS):
            self.set_title("SETTINGS")

        if self.state.is_state(PAUSE_MENU_STATE.AUDIO):
            self.set_title("AUDIO SETTINGS")

        self.draw_title()