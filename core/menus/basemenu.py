from core.ui.font import FontEngine
from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.Audio.Game.state import GAME_SFX_STATE

from helper import log_error
class BaseMenu:
    def __init__(self, window, sound):
        self.window = window
        self.sound = sound
        self.font = FontEngine(90).font
        self.query_font = FontEngine(40).font
        self.type_font = FontEngine(25).font
        self.title = None
        self.query = None
        self.button_action_true_color = (128, 0, 200)
        self.button_action_false_color = (128,128,128)

    def update_toggle_buttons(self):
        if self.buttons:
            for button in self.buttons:
                if button.text.startswith("Music:") and self.sound is not None:
                    button.set_new_text(f"Music: {'On' if self.sound.music_state.is_state(MUSIC_STATE.ON) else 'Off'}")
                elif button.text.startswith("UI SFX:") and self.sound is not None:
                    button.set_new_text(f"UI SFX: {'On' if self.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON) else 'Off'}")
                elif button.text.startswith("Music Vol:") and self.sound is not None:
                    button.set_new_text(f"Music Vol: {int(self.sound.volume*10)}")
                elif button.text.startswith("SFX Vol:") and self.sound is not None:
                    button.set_new_text(f"SFX Vol: {int(self.sound.sfx_volume*10)}")
                elif button.text.startswith("Game SFX:") and self.sound is not None:
                    button.set_new_text(f"Game SFX: {'On' if self.sound.game_sfx_state.is_state(GAME_SFX_STATE.ON) else 'Off'}")

    def set_title(self,text):
        if text == None:
            self.title = None
        else:
            self.title = text

    def set_query(self,text):
        if text == None:
            self.query = None
        else:
            self.query = text

    def draw_title(self):
        if self.title is not None:
            text_color = (255, 255, 255)
            surf = self.font.render(self.title, False, text_color)
            rect = surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 6))
            self.window.blit(surf, rect)
        if self.query is not None:
            text_color = (255, 255, 255)
            surf = self.query_font.render(self.query, False, text_color)
            rect = surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 4))
            self.window.blit(surf, rect)

    def draw_update_text(self):
        text_color = (255, 128,0)
        surf = self.query_font.render("Update Available!", False, text_color)
        rect = surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 3.5))
        self.window.blit(surf, rect)

    def update(self):
        self.update_toggle_buttons()

    def toggle_ui_sfx(self):
        if not self.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.NONE):
            if not self.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                self.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.ON)
            else:
                self.sound.interface_sfx_state.set_state(INTERFACE_SFX_STATE.OFF)
            self.update_toggle_buttons()
        else:
            log_error("No audio device found",f"{self.sound.interface_sfx_state.get_state()}: unable to enable button sound")
            return
        
    def toggle_game_sfx(self):
        if not self.sound.game_sfx_state.is_state(GAME_SFX_STATE.NONE):
            if not self.sound.game_sfx_state.is_state(GAME_SFX_STATE.ON):
                self.sound.game_sfx_state.set_state(GAME_SFX_STATE.ON)
            else:
                self.sound.game_sfx_state.set_state(GAME_SFX_STATE.OFF)
            self.update_toggle_buttons()
        else:
            log_error("No audio device found",f"{self.sound.game_sfx_state.get_state()}: unable to enable button sound")
            return
