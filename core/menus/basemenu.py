from core.ui.font import FontEngine
class BaseMenu:
    def __init__(self, window, sound):
        self.window = window
        self.sound = sound
        self.font = FontEngine(90).font

    def update_toggle_buttons(self):
        for button in self.buttons:
            if button.text.startswith("Music:"):
                button.set_new_text(f"Music: {'On' if self.sound.music_active else 'Off'}")
                    

    def update(self):
        self.update_toggle_buttons()
        