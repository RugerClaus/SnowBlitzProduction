import pygame
from core.ui.button import Button
from core.menus.basemenu import BaseMenu

class Win(BaseMenu):
    def __init__(self, sound, window,restart_callback, main_menu_callback, quit_callback):
        self.window = window
        self.sound = sound
        super().__init__(window, None)
        self.restart_callback = restart_callback
        self.main_menu_callback = main_menu_callback
        self.quit_callback = quit_callback
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.window.get_screen().get_size()
        btn_width, btn_height = screen_w // 4, 50
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7

        center_x = screen_w // 2

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
            self.on_resize()

    def update(self):
        self.on_resize()

    def draw(self):
    
        self.window.draw_overlay((0, 0, 0), 180)

        # Draw "GAME OVER" text
        text = self.font.render("You Win!", True, (80, 80, 248))
        rect = text.get_rect(center=(self.window.get_screen().get_width() // 2, self.window.get_screen().get_height() // 4))
        self.window.get_screen().blit(text, rect)

        # Draw the buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(mouse_pos)
