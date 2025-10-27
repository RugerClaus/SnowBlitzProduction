import pygame

from core.ui.button import Button

class Pause:
    def __init__(self,window,resume_callback,menu_callback,quit_callback,reset_game_callback):
        self.window = window
        self.resume_callback = resume_callback
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.reset_game_callback = reset_game_callback
        self.create_buttons()

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.window.get_screen().get_size()
        btn_width, btn_height = screen_w // 10 + 200, screen_h // 20 + 50
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7

        center_x = screen_w // 2 + screen_w // 4
        unavailable_color = (128,128,150) # placeholder color for buttons that don't currently have implemented functionality
        self.buttons = [
            Button("Resume", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128,0,200), self.resume_callback),
            Button("Main Menu",center_x,start_y + spacing * 1,btn_width,btn_height,(255,255,255),(128,0,200),self.menu_callback),
            Button("Reset Game",center_x,start_y + spacing * 2,btn_width,btn_height,(255,255,255),(128,0,200),self.reset_game_callback),
            Button("Quit", center_x, start_y + spacing * 3, btn_width, btn_height, (255, 255, 255), (128,0,200), self.quit_callback),
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
        pass

    def draw(self):
        self.window.draw_overlay((0,0,0),80)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.window.get_screen(), mouse_pos)
