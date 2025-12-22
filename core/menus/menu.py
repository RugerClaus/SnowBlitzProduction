import pygame
import math
from core.ui.button import Button
from core.guts.animations import Animation
from helper import *

class Menu:
    def __init__(self, screen, endless_callback, blitz_callback, tutorial_callback, quit_callback):
        self.screen = screen
        self.endless_callback = endless_callback
        self.blitz_callback = blitz_callback
        self.tutorial_callback = tutorial_callback
        self.quit_callback = quit_callback

        # Load static assets
        self.title_image_original = pygame.image.load(asset("title")).convert_alpha()
        self.bg_frames_original = asset_frames("frame",14)

        # Initialize UI
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()
        self.bg_frames = []

        # Set up background and buttons
        self.rescale_assets()
        self.background_animation = Animation(self.bg_frames, frame_delay=3)
        self.buttons = []
        self.create_buttons()

    def rescale_assets(self):
        screen_w, screen_h = self.screen.get_size()

        # Rescale background frames from originals
        self.bg_frames = [
            pygame.transform.scale(frame, (screen_w, screen_h))
            for frame in self.bg_frames_original
        ]

        # Rescale title image to half screen width and center it
        new_title_width = int(screen_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = pygame.transform.scale(self.title_image_original, (new_title_width, new_title_height))
        self.title_rect = self.title_image.get_rect(center=(screen_w // 2, int(screen_h * 0.2)))

    def create_buttons(self):
        self.buttons = []
        screen_w, screen_h = self.screen.get_size()
        btn_width, btn_height = screen_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = screen_h // 4 + screen_h // 7

        center_x = screen_w // 2
        unavailable_color = (128,128,150)
        self.buttons = [
            Button("Endless Mode", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128,0,200), self.endless_callback),
            Button("Blitz Mode", center_x, start_y + spacing * 1, btn_width, btn_height, (255, 255, 255), (128,0,200), self.blitz_callback),
            Button("Tutorial", center_x, start_y + spacing * 2, btn_width, btn_height, (255, 255, 255), (128, 128, 128), self.tutorial_callback),
            Button("Quit", center_x, start_y + spacing * 3, btn_width, btn_height, (255, 255, 255), (255, 0, 80), self.quit_callback),
        ]

    def handle_event(self, event,sound_engine):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)

        elif event.type == pygame.VIDEORESIZE:
            self.scale()

    def scale(self):
        self.rescale_assets()
        self.create_buttons()
        self.background_animation.frames = self.bg_frames

    def update(self):
        self.background_animation.update()

    def draw(self):
        t = pygame.time.get_ticks() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.screen.fill(fade_color)

        self.screen.blit(self.background_animation.get_current_frame(), (0, 0))
        self.screen.blit(self.title_image, self.title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
