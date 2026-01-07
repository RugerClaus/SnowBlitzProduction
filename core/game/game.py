import pygame

from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.state.GameLayer.GameMode.statemanager import GameModeManager
from core.game.snowblitz import SnowBlitz
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.menus.pause import Pause
from core.menus.gameover import GameOverMenu
from core.menus.win import Win

class Game:
    def __init__(self, window, sound, menu_callback, quit_callback):
        self.state = GameStateManager()
        self.game_mode = GameModeManager()
        self.window = window
        self.sound = sound
        self.game_object = SnowBlitz(self.window, self.sound, self.state)
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.game_over_menu = GameOverMenu(self.sound,self.window, self.reset_game, self.quit_to_menu, self.quit)
        self.pause_menu = Pause(self.window, self.game_object, self.sound,self.toggle_pause, self.quit_to_menu, self.quit, self.reset_game)
            
    def check_win(self): #this is basically only for the tutorial mode, but needs to be here. no way around it honestly just due to the ease of callback access
        if self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN):
            self.win.update()
            self.win.draw()

    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def resize(self,event_h):
        self.game_object.resize(event_h)
        self.game_over_menu.create_buttons()

    def handle_event(self, event, input):
        input.handle_event(event, True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                if self.state.is_state(GAMESTATE.PAUSED):
                    self.pause_menu.back_to_root()
                    self.toggle_pause()
                else:
                    self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.handle_event()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_7:
                    self.game_object.player.current_level = 15

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if input.last_key == pygame.K_9:
                    self.quit_to_menu()
        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.handle_event(event)
            
        if self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN):
            self.win.handle_event(event)
        

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            if self.game_mode.is_state(GAME_MODE.ENDLESS):
                self.game_object.init_endless()
            elif self.game_mode.is_state(GAME_MODE.BLITZ):
                self.game_object.init_blitz()
            elif self.game_mode.is_state(GAME_MODE.TUTORIAL):
                self.game_over_menu = GameOverMenu(self.sound,self.window,self.reset_tutorial, self.quit_to_menu, self.quit)
                self.pause_menu = Pause(self.window, self.game_object, self.sound,self.toggle_pause, self.quit_to_menu, self.quit, self.reset_tutorial)
                self.win = Win(self.sound,self.window,self.reset_tutorial,self.quit_to_menu,self.quit)
                self.game_object.init_tutorial()
                self.check_win()
        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.update()
            self.game_over_menu.draw()

    def update(self):
        pass

    def run(self):
        self.update()
        self.draw()

    def quit_to_menu(self):
        self.reset_game()
        self.reset_tutorial()
        self.menu_callback()

    def quit(self):
        self.quit_callback()

    def reset_game(self):
        self.game_object.reset()
        self.state.set_state(GAMESTATE.PLAYING)

    def reset_tutorial(self):
        print("resetting tutorial")
        self.game_object.reset_tutorial()
        self.state.set_state(GAMESTATE.PLAYING)

    def set_game_mode(self, mode):
        self.game_mode.set_state(mode)