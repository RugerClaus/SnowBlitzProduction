
from core.application.modes.endless import Endless
from core.application.modes.tutorial.tutorial import Tutorial
from core.application.entities.player.player import Player
from core.application.entities.player.ui.uimanager import PlayerUIManager
from core.application.entities.entitymanager import EntityManager
from core.application.modes.tutorial.tutorialmanager import TutorialManager
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.application.modes.tutorial.prompts import Prompts
from core.state.GameLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.application.entities.type import EntityType
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.application.mechanics.environment.environment import Environment
class SnowBlitz:
    def __init__(self,system,game_state,mode):
        self.system = system
        self.game_state = game_state
        self.mode = mode

        self.endless = None
        self.tutorial = None
        self.blitz = None

        self.entitymanager = EntityManager(system)
        
        self.start_time = system.time.get_current_time()
        self.player = None
        self.progress_bar = None
        self.endless = None
        self.tutorial_manager = None
        self.prompts = None
        self.blitz = None
        self.tutorial_state = None

        self.draw_debug_snowflake_lines = False
        self.draw_debug_rock_lines = False
        self.draw_debug_powerup_lines = False
        self.draw_debug_reducer_lines = False

        self.environment = Environment(system)

    def toggle_debug_snowflake_lines(self):
        self.draw_debug_snowflake_lines = not self.draw_debug_snowflake_lines

    def toggle_debug_rock_lines(self):
        self.draw_debug_rock_lines = not self.draw_debug_rock_lines

    def toggle_debug_powerup_lines(self):
        self.draw_debug_powerup_lines = not self.draw_debug_powerup_lines

    def toggle_debug_reducer_lines(self):
        self.draw_debug_reducer_lines = not self.draw_debug_reducer_lines

    def handle_event(self):

        keys = self.system.input.get_pressed_keys()
        if self.player is not None:
            if not keys[self.system.input.game_controls.slow]:
                if keys[self.system.input.game_controls.move_left]:
                    self.player.move('LEFT')
                elif keys[self.system.input.game_controls.move_right]:
                    self.player.move('RIGHT')
            else:
                if keys[self.system.input.game_controls.move_left]:
                    self.player.move('SLOW_LEFT')
                elif keys[self.system.input.game_controls.move_right]:
                    self.player.move('SLOW_RIGHT')
            if not (keys[self.system.input.game_controls.move_left] or keys[self.system.input.game_controls.move_right]):
                self.player.move('NONE')
        else:
            print("error can't process input")
        
    def draw_vector_lines(self):
        if not self.mode.is_state(GAME_MODE.NONE):
            for entity in self.entitymanager.get_active_entities():
                if self.draw_debug_snowflake_lines:
                    if entity.type == EntityType.SNOWFLAKE:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.player.rect.center,(255,0,0))
                if self.draw_debug_rock_lines:    
                    if entity.type == EntityType.ROCK:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.player.rect.center,(0,255,0))
                if self.draw_debug_powerup_lines:    
                    if entity.type == EntityType.POWERUP:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.player.rect.center,(255,255,255))
                if self.draw_debug_reducer_lines:
                    if entity.type == EntityType.REDUCER:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.player.rect.center,(0,0,255))

    def init_player(self):
        if self.player is None:
            self.player = Player(self.system,self.entitymanager,self.game_state,self.environment)
        if self.progress_bar is None:
            self.progress_bar = PlayerUIManager(self.system,self.player)

    def init_tutorial(self):
        self.init_player()
        if self.prompts is None:
            self.prompts = Prompts(self.system.window,self.player,self.system.input)
        if self.tutorial_state is None:
            self.tutorial_state = TutorialStateManager()
        if self.tutorial_manager is None: 
            self.tutorial_manager = TutorialManager(self.system.window, self.prompts,self.system.input.game_controls,
                                                self.entitymanager,self.player,self.progress_bar,self.tutorial_state)
        if self.tutorial is None:
            self.tutorial = Tutorial(self.system.window,self.player,self.entitymanager,self.system.input.game_controls,
                                                self.progress_bar,self.tutorial_state,self.tutorial_manager,self.prompts)

    def init_endless(self):
        self.init_player()
        if self.endless is None:
            self.endless = Endless(self.progress_bar, self.player, self.entitymanager)

    def draw(self):
        self.environment.update()
        self.environment.draw()
        if self.mode.is_state(GAME_MODE.ENDLESS):
            
                self.init_endless()
                self.endless.run()
        elif self.mode.is_state(GAME_MODE.TUTORIAL):
            self.init_tutorial()
            self.tutorial.run()
        elif self.mode.is_state(GAME_MODE.BLITZ):
            if self.blitz is None:
                pass
            self.blitz.run()

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.draw_vector_lines()

    def resize(self, event_h):
        if self.player is not None:
            self.player.scale(event_h)
            self.player.center()
        if self.progress_bar is not None:
            self.progress_bar.update()
            self.progress_bar.draw()

    def clean_up_states(self):
        self.system.clean_up_states([self.player.speed_state.state,self.player.move_state.state,self.player.power_state.state,self.player.life_state.state])
        if self.tutorial_state is not None:
            self.system.clean_up_states([self.tutorial_state.state])

    def register_debug_telemetry(self):
        self.system.runtime_inspector["daytime"] = self.environment.day_cycle.get_daytime()
        self.system.runtime_inspector["brightness"] = self.environment.day_cycle.get_brightness()
        self.system.runtime_inspector["temperature"] = self.environment.temperature.get_temperature()
        if self.player:
            self.system.runtime_inspector["shrinkrate"] = self.player.shrink_rate

    def reset_systems(self):
        del self.player
        del self.progress_bar
        del self.endless
        del self.tutorial
        del self.tutorial_state
        del self.tutorial_manager
        del self.prompts
        del self.blitz
        self.player = None
        self.progress_bar = None
        self.endless = None
        self.tutorial = None
        self.tutorial_state = None
        self.tutorial_manager = None
        self.prompts = None
        self.blitz = None
        self.environment.day_cycle.reset()
        
    def reset(self):
        if self.player is not None:
            self.player.reset()

        if self.progress_bar is not None:
            self.progress_bar.reset_timer()
            self.progress_bar.draw()

        self.entitymanager.reset_entities()
        self.entitymanager.reset_spawn_timers()

        self.reset_systems()