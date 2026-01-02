import pygame
import math
from core.menus.basemenu import BaseMenu
from core.ui.button import Button
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.game.entities.player.ui.sizebar import SizeBar
from core.state.GameLayer.state import GAMESTATE

class Pause(BaseMenu):
    def __init__(self, window, game, sound, resume_callback, menu_callback, quit_callback, reset_game_callback):
        self.window = window
        self.sound = sound
        self.game = game
        super().__init__(window, sound)
        self.resume_callback = resume_callback
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.reset_game_callback = reset_game_callback
        self.state = MenuStateManager()
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.window.get_screen().get_size()
        btn_width, btn_height = screen_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7
        center_x = screen_w // 2

        if self.state.is_state(MENUSTATE.ROOT):
            self.buttons = [
                Button("Resume", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.resume_callback),
                Button("Main Menu", center_x, start_y + spacing * 1, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.menu_callback),
                Button("Reset Game", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.reset_game_callback),
                Button("Settings", center_x, start_y + spacing * 3, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.go_to_settings),
                Button("Quit", center_x, start_y + spacing * 4, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.quit_callback),
            ]
        elif self.state.is_state(MENUSTATE.SETTINGS):
            self.buttons = [
                Button(f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.audio_settings),
                Button(f"Progress Bar: ", center_x, start_y + spacing * 1, btn_width * 1.8, btn_height, (255, 255, 255), (128, 0, 200), self.game.progress_bar.toggle_location),
                Button("Back", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.back_to_root),
            ]

        elif self.state.is_state(MENUSTATE.AUDIO):
            self.buttons = [
                Button(f"+", center_x, self.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_up),
                Button(f"-", center_x, self.window.get_height() // 2 + spacing * 0.4, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_down),
                Button(f"Music: {'On' if self.sound.music_active else 'Off'}", center_x, self.window.get_height() // 2 + spacing * 1.5, 200, btn_height,
                    (255, 255, 255), (128, 0, 200), self.sound.toggle_music),
                Button("Back", center_x, self.window.get_height() // 2 + spacing * 2.5, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.go_to_settings)
            ]

    def update_toggle_buttons(self):
        for button in self.buttons:
            if button.text.startswith("Music:"):
                button.set_new_text(f"Music: {'On' if self.sound.music_active else 'Off'}")
            if button.text.startswith("Progress Bar:"):
                button.set_new_text(f"Progress Bar: {'Top' if self.game.progress_bar.location == SizeBar.TOP else 'Bottom'}")
                

    def update(self):
        self.update_toggle_buttons()
        if self.game.game_state.is_state(GAMESTATE.PLAYING):
            self.back_to_root()

    def reset_menu(self):
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def audio_settings(self):
        self.state.set_state(MENUSTATE.AUDIO)
        self.create_buttons()

    def back_to_root(self):
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def go_to_settings(self):
        self.state.set_state(MENUSTATE.SETTINGS)
        self.create_buttons()

    def on_resize(self):
        self.create_buttons()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)

        elif event.type == pygame.VIDEORESIZE:
            self.on_resize()

    def draw(self):
        t = pygame.time.get_ticks() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            0,
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.window.fill(fade_color)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.window.get_screen(), mouse_pos)

        self.set_title("PAUSED")

        if self.state.is_state(MENUSTATE.SETTINGS):
            self.set_title("SETTINGS")

        if self.state.is_state(MENUSTATE.AUDIO):
            self.set_title("AUDIO SETTINGS")
            self.audio_text.draw(self.sound.volume)

        self.draw_title()