import pygame,math
from core.ui.button import Button
from core.menus.basemenu import BaseMenu

from helper import *

class GameOverMenu(BaseMenu):
    def __init__(self, sound, window, restart_callback, main_menu_callback, quit_callback):
        self.window = window
        self.sound = sound
        super().__init__(window, self.sound)
        self.restart_callback = restart_callback
        self.main_menu_callback = main_menu_callback
        self.quit_callback = quit_callback
        self.create_buttons()

    def create_buttons(self):
        window_w, window_h = self.window.get_size()
        btn_width, btn_height = window_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = window_h // 4 + window_h // 7
        center_x = window_w // 2

        self.buttons = [
            Button(self.sound, self.window, "Restart", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.restart_callback),
            Button(self.sound, self.window, "Main Menu", center_x, start_y + spacing, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.main_menu_callback),
            Button(self.sound, self.window, "Quit", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.quit_callback),
        ]

    def on_resize(self):
        self.create_buttons()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == pygame.VIDEORESIZE:
            self.window.get_size()
            self.create_buttons()

    def draw(self):
        t = self.window.get_current_time() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.window.fill(fade_color)

        text = self.font.render("GAME OVER", True, (255, 0, 0))
        rect = text.get_rect(center=(self.window.get_screen().get_width() // 2, self.window.get_screen().get_height() // 4))
        self.window.get_screen().blit(text, rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(mouse_pos)
