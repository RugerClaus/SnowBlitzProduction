import pygame

from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.Loading.state import LOAD_SCREEN_STATE
from core.state.ApplicationLayer.Loading.statemanager import LoadingStateManager
from helper import asset

class LoadingManager:
    def __init__(self,window,parent_state,sound):
        self.window = window
        self.parent_state = parent_state
        self.sound = sound
        self.sound.play_sfx('splash')
        self.state = LoadingStateManager()
        self.title_image_original = self.window.load_image(asset("splash")).convert_alpha()
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect(center=(self.window.get_width()//2,self.window.get_height()//2))
        self.start_time = self.window.get_current_time()
        self.state.set_state(LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN)

    def rescale_assets(self):
        window_w, window_h = self.window.get_size()
        self.title_rect = self.title_image.get_rect(center=(window_w // 2, window_h // 2 - 50))

    def update(self):
        if self.state.is_state(LOAD_SCREEN_STATE.NONE):
            self.parent_state.set_state(APPSTATE.MAIN_MENU)
            self.sound.play_music()
        if not self.parent_state.is_state(APPSTATE.LOADING):
            self.state.set_state(LOAD_SCREEN_STATE.NONE)
            self.sound.play_music()

    def draw(self):
        current_time = self.window.get_current_time()
        if self.state.is_state(LOAD_SCREEN_STATE.STUDIO_SPLASH_SCREEN):
            if current_time - self.start_time > 3500 or not self.parent_state.is_state(APPSTATE.LOADING):
                self.state.set_state(LOAD_SCREEN_STATE.NONE)
            else:
                self.window.blit(self.title_image,self.title_rect)
