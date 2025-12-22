import pygame

from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.state.GameLayer.GameMode.statemanager import GameModeManager
from core.game.snowblitz import SnowBlitz
from core.menus.pause import Pause
from helper import asset,get_colors

class Game:
    def __init__(self,window,sound,menu_callback,quit_callback):

        self.state = GameStateManager()
        self.game_mode = GameModeManager()
        self.window = window
        self.surface = window.make_surface(window.get_width(),window.get_height(),True)
        self.sound = sound
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.pause_menu = Pause(window,self.toggle_pause,self.quit_to_menu,self.quit,self.reset)
        self.intent = None
        self.game_object = SnowBlitz(self.surface,self.sound)

    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def handle_event(self,event,input):
        input.handle_event(event,True)
        if event.type == pygame.VIDEORESIZE:
            self.surface = self.window.make_surface(self.window.get_width(),self.window.get_height(),True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            if event.type == pygame.KEYDOWN:
                pass
                

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if input.last_key == pygame.K_9:
                    self.quit_to_menu()
        
    def set_mode(self,mode):
        if mode == 'ENDLESS':
            self.game_mode.set_state(GAME_MODE.ENDLESS)
        if mode == 'BLITZ':
            self.game_mode.set_state(GAME_MODE.BLITZ)
        if mode == 'TUTORIAL':
            self.game_mode.set_state(GAME_MODE.TUTORIAL)
        if mode == 'QUIT_TO_MENU':
            self.game_mode.set_state(GAME_MODE.NONE)

    def draw(self):

        self.window.blit(self.surface,(0,0))
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.init_endless()
        
        
    def update(self):
        pass

    def run(self):

        self.update()
        self.draw()
        

    def quit_to_menu(self):
        self.reset()
        pygame.event.clear()
        self.menu_callback()

    def quit(self):
        self.quit_callback()
    
    def reset(self):
        self.state.set_state(GAMESTATE.PLAYING)

