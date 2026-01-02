import pygame
import math
from core.menus.basemenu import BaseMenu
from core.ui.button import Button
from helper import *
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.menus.credits import Credits

class Menu(BaseMenu):
    def __init__(self, screen, sound, endless_callback, blitz_callback, tutorial_callback, quit_callback):
        self.screen = screen
        self.sound = sound
        super().__init__(screen, sound)
        self.endless_callback = endless_callback
        self.blitz_callback = blitz_callback
        self.tutorial_callback = tutorial_callback
        self.quit_callback = quit_callback
        self.state = MenuStateManager()
        self.credits = Credits(self.screen)

        self.title_image_original = pygame.image.load(asset("title")).convert_alpha()
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()
        

        self.create_buttons()
        self.rescale_assets()

    def rescale_assets(self):
        screen_w, screen_h = self.screen.get_size()
        new_title_width = int(screen_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = pygame.transform.scale(self.title_image_original, (new_title_width, new_title_height))
        self.title_rect = self.title_image.get_rect(center=(screen_w // 2, int(screen_h * 0.2)))
        self.credits.rescale()

    def create_buttons(self):
        screen_w, screen_h = self.screen.get_size()
        btn_width, btn_height = screen_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7
        center_x = screen_w // 2

        if self.state.is_state(MENUSTATE.ROOT):
            self.buttons = [
                Button("Endless Mode", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.endless_callback),
                Button("Blitz Mode", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.blitz_callback),
                Button("Tutorial", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), (128, 128, 128), self.tutorial_callback),
                Button("Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.go_to_settings),
                Button("Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), (255, 0, 80), self.quit_callback),
                Button("Credits", screen_w - screen_w // 8, screen_h - 100, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.credits_callback),
            ]
        elif self.state.is_state(MENUSTATE.SETTINGS):
            self.buttons = [
                Button(f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.audio_settings),
                Button("Back", center_x, start_y + spacing * 1, btn_width, btn_height,
                    (255, 255, 255), (255, 0, 80), self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.CREDITS):

            self.buttons = [
                Button("Back", screen_w - screen_w // 8, screen_h - 100, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.back_to_root),
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

    def credits_callback(self):
        self.state.set_state(MENUSTATE.CREDITS)
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

    def handle_event(self, event, sound_engine):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == pygame.VIDEORESIZE:
            self.scale()

    def scale(self):
        self.rescale_assets()
        self.create_buttons()

    def draw(self):
        t = pygame.time.get_ticks() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.screen.fill(fade_color)

        

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)

        if self.state.is_state(MENUSTATE.ROOT):
            self.set_title(None)
            self.screen.blit(self.title_image, self.title_rect)

        if self.state.is_state(MENUSTATE.SETTINGS):
            self.set_title("SETTINGS")

        if self.state.is_state(MENUSTATE.CREDITS):
            self.credits.draw()

        if self.state.is_state(MENUSTATE.AUDIO):
            self.set_title("AUDIO SETTINGS")
            self.audio_text.draw(self.sound.volume)
        
        self.draw_title()