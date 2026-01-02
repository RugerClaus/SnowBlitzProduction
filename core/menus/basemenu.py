from core.ui.font import FontEngine
from core.menus.audio import Audio
class BaseMenu:
    def __init__(self, window, sound):
        self.window = window
        self.sound = sound
        self.font = FontEngine(90).font
        self.audio_text = Audio(self.window)
        self.title = None

    def update_toggle_buttons(self):
        for button in self.buttons:
            if button.text.startswith("Music:") and self.sound is not None:
                button.set_new_text(f"Music: {'On' if self.sound.music_active else 'Off'}")
            elif button.text.startswith("SFX:") and self.sound is not None:
                button.set_new_text(f"SFX: {'On' if self.sound.active_sfx else 'Off'}")

    def set_title(self,text):
        if text == None:
            self.title = None
        else:
            self.title = text

    def draw_title(self):
        if self.title is not None:
            text_color = (255, 255, 255)
            surf = self.font.render(self.title, False, text_color)
            rect = surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 4))
            self.window.blit(surf, rect)

    def update(self):
        self.update_toggle_buttons()