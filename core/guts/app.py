import pygame, sys
from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.statemanager import StateManager
from core.state.ApplicationLayer.mode import APPMODE
from core.state.ApplicationLayer.modemanager import ModeManager
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.devmanager import DevManager
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.util.debugger import Debugger
from core.guts.input.inputmanager import InputManager
from core.game.game import Game
from core.menus.menu import Menu
from core.guts.audioengine import AudioEngine
from core.loading.loadingmanager import LoadingManager

class App:
    def __init__(self,window):

        self.window = window
        self.input = InputManager(window)
        self.state = StateManager()
        self.mode = ModeManager()
        self.dev = DevManager()
        self.sound = AudioEngine()
        self.menu = Menu(window,self.sound,self.endless,self.blitz,self.tutorial,self.quit)
        self.game = Game(window,self.sound,self.go_to_menu,self.quit)
        self.loading = LoadingManager(self.window,self.state,self.sound)
        self.debugger = Debugger(self.game,self.state,window,self.sound,self.loading)

    def _popup_test_toggle(self):
        self.popup_active = not self.popup_active

    def endless(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode(GAME_MODE.ENDLESS)
    
    def blitz(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode(GAME_MODE.BLITZ)
    
    def tutorial(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode(GAME_MODE.TUTORIAL)

    def toggle_debug_mode(self):
        if not self.mode.is_state(APPMODE.DEBUG):
            self.mode.set_state(APPMODE.DEBUG)
        else:
            self.mode.set_state(APPMODE.PRIMARY)

    def toggle_developer_mode(self):
        if not self.dev.is_state(DEVELOPER_MODE.ON):
            self.dev.set_state(DEVELOPER_MODE.ON)
        else:
            self.dev.set_state(DEVELOPER_MODE.OFF)

    def quit(self):
        self.state.set_state(APPSTATE.QUIT)

    def go_to_menu(self):
        self.state.set_state(APPSTATE.MAIN_MENU)
        self.game.reset_game()
        self.game.game_mode.set_state(GAME_MODE.NONE)
        self.menu.scale()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.window.scale(event.w,event.h)
                self.debugger.scale()
                self.loading.rescale_assets()
                self.menu.scale()
                self.input.rescale(event.w,event.h)
                if not self.state.is_state(APPSTATE.IN_GAME):
                    self.game.resize(event.h)

            if event.type == pygame.QUIT:
                self.state.set_state(APPSTATE.QUIT)
            
            if self.state.is_state(APPSTATE.MAIN_MENU):
                self.menu.handle_event(event,self.sound.volume)

            elif self.state.is_state(APPSTATE.IN_GAME):
                self.game.handle_event(event,self.input)
            
            if self.mode.is_state(APPMODE.DEBUG):
                self.debugger.handle_event(event)

            self.sound.handle_music_event(event)
            
            command = self.input.handle_event(event)
            if command == "debug":
                self.toggle_debug_mode()
            
            elif command == "developer":
                self.toggle_developer_mode()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.window.toggle_fullscreen()
                if self.state.is_state(APPSTATE.LOADING):
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.state.set_state(APPSTATE.MAIN_MENU)
                        self.sound.play_music()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state.is_state(APPSTATE.LOADING):
                    self.state.set_state(APPSTATE.MAIN_MENU)
                    self.sound.play_music()

    def run(self):
        while not self.state.is_state(APPSTATE.QUIT):
            self.window.fill((0,0,0))
            self.handle_events()

            if self.state.is_state(APPSTATE.LOADING):
                self.loading.update()
                self.loading.draw()
            
            elif self.state.is_state(APPSTATE.MAIN_MENU):
                self.menu.update()
                self.menu.draw()
            elif self.state.is_state(APPSTATE.IN_GAME):
                self.game.run()
            elif self.state.is_state(APPSTATE.QUIT):
                sys.exit()

            if self.mode.is_state(APPMODE.DEBUG):
                self.debugger.update()
                self.debugger.draw()
                self.input.draw_most_recent_keypress()
            
            if self.dev.is_state(DEVELOPER_MODE.ON):
                pass

            self.window.timer()
            self.window.update()