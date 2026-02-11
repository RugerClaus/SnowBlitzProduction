from helper import log_event, log_error
from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.GameLayer.GameMode.statemanager import GameModeManager
from core.game.snowblitz import SnowBlitz
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.menus.pause import Pause
from core.menus.gameover import GameOverMenu
from core.menus.win import Win

class Game:
    def __init__(self, window, sound, input, dev_mode, menu_callback, quit_callback):
        self.state = GameStateManager()
        self.game_mode = GameModeManager()
        self.window = window
        self.sound = sound
        self.input = input
        self.dev_mode = dev_mode
        self.game_object = SnowBlitz(self.window, self.sound, self.state,self.input,self.game_mode)
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.game_over_menu = GameOverMenu(self.sound,self.window, self.input, self.reset_game, self.quit_to_menu, self.quit)
        self.pause_menu = Pause(self.window, self.game_object, self.sound, self.input, self.toggle_pause, self.quit_to_menu, self.quit, self.reset_game)
            
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

    def handle_event(self, event, input):

        if event.type == self.input.keydown():
            if self.input.get_key_name(event.key) == "escape":
                
                if self.state.is_state(GAMESTATE.PAUSED):
                    self.pause_menu.back_to_root()
                    self.toggle_pause()
                else:
                    self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.handle_event()
            if event.type == self.input.keydown():
                if self.dev_mode.is_state(DEVELOPER_MODE.ON):
                    if self.input.get_key_name(event.key) == "7":
                        self.game_object.player.current_level = 15

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)

        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.handle_event(event)
            
        if self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN):
            self.win.handle_event(event)
        
        if event.type == self.input.video_resize_event():
            self.game_over_menu.create_buttons()
            self.pause_menu = Pause(self.window, self.game_object, self.sound, self.input,  self.toggle_pause, self.quit_to_menu, self.quit, self.reset_tutorial)
            self.win = Win(self.sound,self.window,self.input,self.reset_tutorial,self.quit_to_menu,self.quit)
            self.resize(event.h)    
        

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.draw()
            
        elif self.state.is_state(GAMESTATE.GAME_OVER):
            
            self.game_over_menu.draw()

    def update(self):
        self.game_over_menu.update()

    def run(self):
        self.update()
        self.draw()

    def quit_to_menu(self):
        self.reset_game()
        self.menu_callback()

    def quit(self):
        self.quit_callback()

    def reset_game(self):
        self.game_object.reset()
        self.state.set_state(GAMESTATE.PLAYING)

    def reset_tutorial(self):
        log_event("resetting tutorial")
        self.state.set_state(GAMESTATE.PLAYING)

    def set_game_mode(self, mode):
        self.game_mode.set_state(mode)