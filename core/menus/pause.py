import pygame
import math
from core.menus.basemenu import BaseMenu
from core.ui.button import Button
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.game.entities.player.ui.sizebar import SizeBar

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
                Button(f"Music: {'On' if self.sound.music_active else 'Off'}", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.sound.toggle_music),
                Button(f"Progress Bar: {'Top' if self.game.progress_bar.location == SizeBar.TOP else 'Bottom'}", center_x, start_y + spacing * 1, btn_width * 1.8, btn_height, (255, 255, 255), (128, 0, 200), self.game.progress_bar.toggle_location),
                Button("Back", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.back_to_root),
            ]

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
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.window.fill(fade_color)

        text_color = (255, 255, 255)
        paused_text = "PAUSED"
        paused_surf = self.font.render(paused_text, False, text_color)
        paused_rect = paused_surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 4))

        self.window.blit(paused_surf, paused_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.window.get_screen(), mouse_pos)
