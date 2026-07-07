from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.GameLayer.GameMode.statemanager import GameModeManager
from core.application.snowblitz import SnowBlitz
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.menus.pause import Pause
from core.menus.gameover import GameOverMenu
from core.menus.win import Win

class Game:
    def __init__(self, system):
        self.state = GameStateManager()
        self.game_mode = GameModeManager()
        self.system = system
        self.game_object = SnowBlitz(system,self.state,self.game_mode)
        self.game_over_menu = GameOverMenu(system, self.reset_game)
        self.pause_menu = Pause(system, self.game_object, self,self.toggle_pause, self.reset_game)
        self.win = Win(self.system,self.reset_game)

    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def resize(self,event_h):
        self.game_object.resize(event_h)

    def send_debug_info_to_system(self):
        self.system.runtime_inspector["daytime"] = self.game_object.environment.day_cycle.get_daytime()
        self.system.runtime_inspector["brightness"] = self.game_object.environment.day_cycle.get_brightness()
        self.system.runtime_inspector["temperature"] = self.game_object.environment.temperature.get_temperature()
        if self.game_object.player:
            self.system.runtime_inspector["shrinkrate"] = self.game_object.player.shrink_rate

    def remove_debug_info_from_system(self):
        self.system.runtime_inspector["daytime"] = None
        self.system.runtime_inspector["brightness"] = None
        self.system.runtime_inspector["shrinkrate"] = None 
        self.system.runtime_inspector["temperature"] = None

    def handle_event(self, event):

        if event.type == self.system.input.keydown():
            if self.system.input.get_key_name(event.key) == "escape":
                
                if self.state.is_state(GAMESTATE.PAUSED):
                    self.pause_menu.back_to_root()
                    self.toggle_pause()
                else:
                    self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.handle_event()
            if event.type == self.system.input.keydown():
                if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                    if event.key == self.system.input.keys.seven_key():
                        self.game_object.player.current_level = 19
                    
                    elif event.key == self.system.input.keys.h_key():
                        self.game_object.player.current_level = 15

                    elif event.key == self.system.input.keys.F3_key():
                        self.game_object.toggle_debug_snowflake_lines()

                    elif event.key == self.system.input.keys.F4_key():
                        self.game_object.toggle_debug_rock_lines()
                    
                    elif event.key == self.system.input.keys.F5_key():
                        self.game_object.toggle_debug_powerup_lines()
                        
                    elif event.key == self.system.input.keys.F6_key():
                        self.game_object.toggle_debug_reducer_lines()

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)

        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.handle_event(event)
            self.system.sound.stop_all_sfx()
            
        if self.game_object.tutorial_state is not None and self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN):
            self.win.handle_event(event)
        
        if event.type == self.system.input.video_resize_event():
            self.game_over_menu.create_buttons()
            self.pause_menu.create_buttons()
            self.win.create_buttons()
            self.resize(event.h)    
        

    def draw(self):
        if not self.state.is_state(GAMESTATE.NONE) and self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.draw()
        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.draw()
        elif self.state.is_state(GAMESTATE.WIN):
            self.win.draw()

    def update(self):
        self.win.update()
        self.send_debug_info_to_system()
        self.game_over_menu.update()
        if self.game_object.tutorial_state is not None:
            if self.game_object.tutorial_state and self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN):
                self.state.set_state(GAMESTATE.WIN)

        if self.game_object.player:
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.game_object.player.shrink_rate = 0

    def run(self):
        self.update()
        self.draw()

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.reset_game()
        self.state.set_state(GAMESTATE.NONE)
        self.game_mode.set_state(GAME_MODE.NONE)
        self.system.go_to_menu()
        

    def quit(self):
        self.system.quit()

    def reset_game(self):
        self.game_object.reset()
        self.state.set_state(GAMESTATE.PLAYING)

    def set_game_mode(self, mode):
        self.game_mode.set_state(mode)
        self.system.sound.play_music()