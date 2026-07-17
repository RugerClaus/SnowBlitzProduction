from core.state.ApplicationLayer.state import GAMESTATE
from core.state.ApplicationLayer.statemanager import GameStateManager
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.ApplicationLayer.GameMode.statemanager import GameModeManager
from core.application.snowblitz import SnowBlitz
from core.state.ApplicationLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.menus.pause import Pause
from core.menus.gameover import GameOverMenu
from core.menus.win import Win


class Game:

    def __init__(self, system):
        self.system = system
        self.state = GameStateManager()
        self.state.set_state(GAMESTATE.PLAYING)
        self.game_mode = GameModeManager()
        self.game_object = SnowBlitz(system,self.state,self.game_mode)
        self.pause_menu = Pause(self.system,self.game_object,self.toggle_pause,self.reset_game)
        self.game_over_menu = GameOverMenu(self.system,self.reset_game)
        self.win = Win(system,self.reset_game)

    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.reset_menu()
            self.state.set_state(GAMESTATE.PAUSED)

        else:
            self.game_object.environment.day_cycle.resume()
            self.state.set_state(GAMESTATE.PLAYING)
            
    def handle_event(self, event):
        if event.type == self.system.input.window_focus_lost():
            self.state.set_state(GAMESTATE.PAUSED)
        if event.type == self.system.input.keydown():
            if event.key == self.system.input.keys.escape_key():
                if self.state.is_state(GAMESTATE.PAUSED):
                    self.pause_menu.back_to_root()

                self.toggle_pause()


        if self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.handle_event()

            if event.type == self.system.input.keydown():
                if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                    self.game_object.debug.handle_event(event)

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)

        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.handle_event(event)

        elif self.state.is_state(GAMESTATE.WIN):
            self.win.handle_event(event)

        if event.type == self.system.input.video_resize_event():
            self.pause_menu.create_buttons()
            self.game_over_menu.create_buttons()
            self.win.create_buttons()
            self.resize(event)
        if (self.game_object.tutorial_state is not None and self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN)):
            self.win.handle_event(event)

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.game_object.draw()
            self.pause_menu.draw()

        elif self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.draw()

        elif self.state.is_state(GAMESTATE.GAME_OVER):
            self.game_over_menu.update()
            self.game_over_menu.draw()

        elif self.state.is_state(GAMESTATE.WIN):
            self.win.draw()

    def update(self):
        self.send_debug_info_to_system()
        if (self.game_object.tutorial_state and self.game_object.tutorial_state.is_state(TUTORIALSTATE.WIN)):
            self.state.set_state(GAMESTATE.WIN)
            self.win.update()

        if self.game_object.player:
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.game_object.player.shrink_rate = 0

        if self.state.is_state(GAMESTATE.PLAYING):
            self.game_object.update()

        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()

    def resize(self,event):
        self.game_object.resize(event)



    def reset_game(self):
        self.game_object.reset()
        self.state.set_state(GAMESTATE.PLAYING)


    def set_game_mode(self, mode=None):
        if mode:
            self.game_mode.set_state(mode)

        else:
            self.state.set_state(GAMESTATE.PLAYING)
            self.game_mode.set_state(self.game_object.endless_state)
        self.system.sound.play_music()

    def quit_to_menu(self):
        self.remove_debug_info_from_system()
        self.game_object.clean_up_states()
        self.game_object.reset()

    def quit(self):
        self.system.quit()

    def send_debug_info_to_system(self):
        self.game_object.register_debug_telemetry()

    def remove_debug_info_from_system(self):
        self.system.app_inspector.clear()