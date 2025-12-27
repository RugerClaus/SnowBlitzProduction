import pygame, sys
from core.state.ApplicationLayer.state import APPSTATE
from core.state.ApplicationLayer.statemanager import StateManager
from core.state.ApplicationLayer.mode import APPMODE
from core.state.ApplicationLayer.modemanager import ModeManager
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.util.debugger import Debugger
from core.guts.input.inputmanager import InputManager
from core.game.game import Game
from core.menus.menu import Menu
from core.guts.audioengine import AudioEngine

class App:
    def __init__(self,window):

        self.window = window
        self.input = InputManager(window)
        self.state = StateManager()
        self.mode = ModeManager()
        self.app_volume = 0.5
        self.sound = AudioEngine(self.app_volume)
        self.menu = Menu(window.get_screen(),self.sound,self.endless,self.blitz,self.tutorial,self.quit)
        self.game = Game(window,self.sound,self.go_to_menu,self.quit)
        self.debugger = Debugger(self.game,self.state,window,self.sound)
        self.sound.play_music()

    def _popup_test_toggle(self):
        self.popup_active = not self.popup_active

    def endless(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode('ENDLESS')
    
    def blitz(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode('BLITZ')
    
    def tutorial(self):
        self.state.set_state(APPSTATE.IN_GAME)
        self.game.set_game_mode('TUTORIAL')

    def toggle_debug_mode(self):
        if not self.mode.is_state(APPMODE.DEBUG):
            self.mode.set_state(APPMODE.DEBUG)
        else:
            self.mode.set_state(APPMODE.PRIMARY)
    def quit(self):
        self.state.set_state(APPSTATE.QUIT)

    def go_to_menu(self):
        self.state.set_state(APPSTATE.MAIN_MENU)
        self.game.game_mode.set_state(GAME_MODE.NONE)
        self.menu.scale()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.window.scale(event.w,event.h)
                self.debugger.scale()
                if self.state.is_state(APPSTATE.MAIN_MENU):
                    self.menu.scale()


            if event.type == pygame.QUIT:
                self.state.set_state(APPSTATE.QUIT)
            
            if self.state.is_state(APPSTATE.MAIN_MENU):
                self.menu.handle_event(event,self.sound.volume)

            elif self.state.is_state(APPSTATE.IN_GAME):
                self.game.handle_event(event,self.input)
            
            if self.mode.is_state(APPMODE.DEBUG):
                self.debugger.handle_event(event)

            command = self.input.handle_event(event)
            if command == "debug":
                self.toggle_debug_mode()

            # This one is a test for outputting data to the console via an in game command.
            # Another feature of the input buffer (IOSTREAM ;^)
            elif command == "secret":
                print("Kiss me!")

            # This one is just a test, but I'll probably implement an entire debug 
            # menu. I'll write some functionality ideas here when I have them.
            # ...
            
            # And here is an actual practical use of this engine. It was very smooth to implement
            # by itself.
            elif command == "musicon":
                
                self.sound.play_music()
            
            elif command == "musicoff":
                self.sound.play_music('stop')
                
    
    def run(self):
        while not self.state.is_state(APPSTATE.QUIT):
            self.window.fill((0,0,0))
            self.handle_events()
            
            
            if self.state.is_state(APPSTATE.MAIN_MENU):
                self.menu.update()
                self.menu.draw()
            elif self.state.is_state(APPSTATE.IN_GAME):
                self.game.run()
            elif self.state.is_state(APPSTATE.QUIT):
                pygame.quit()
                sys.exit()

            if self.mode.is_state(APPMODE.DEBUG):
                self.debugger.update()
                self.debugger.draw()
                self.input.draw_most_recent_keypress()

            self.window.timer()
            self.window.update()