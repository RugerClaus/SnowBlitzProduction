
from core.application.modes.endless import Endless
from core.application.modes.tutorial.tutorial import Tutorial
from core.application.entities.player.player import Player
from core.application.entities.player.ui.uimanager import PlayerUIManager
from core.application.entities.entitymanager import EntityManager
from core.application.modes.tutorial.tutorialmanager import TutorialManager
from core.application.modes.tutorial.prompts import Prompts
from core.state.ApplicationLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager
from core.state.ApplicationLayer.GameMode.state import GAME_MODE
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.application.mechanics.environment.environment import Environment
from core.application.debug.sbdebugutils import SBDebugUtils
from core.application.network.sessions import Session
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE
class SnowBlitz:
    def __init__(self,system,game_state,mode):
        self.system = system
        self.game_state = game_state
        self.mode = mode

        self.endless = None
        self.tutorial = None
        self.blitz = None

        self.entitymanager = EntityManager(system)
        self.debug = SBDebugUtils(system,self)
        
        self.start_time = system.time.get_current_time()
        self.player = None
        self.progress_bar = None
        self.endless = None
        self.tutorial_manager = None
        self.prompts = None
        self.blitz = None
        self.tutorial_state = None

        self.environment = Environment(system)

        self.endless_state = GAME_MODE.ENDLESS
        self.session = Session(system)
        self.session.start_online_session()

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
            pass

    def init_player(self):
        if self.player is None:
            self.player = Player(self.system,self.entitymanager,self.game_state,self.environment,self.session)
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
            self.debug.draw()
            if self.session.state.is_state(ONLINE_SESSION_STATE.ACTIVE):
                self.session.end_online_session()
            

    def resize(self, event_h):
        if self.player is not None:
            self.player.scale(event_h)
            self.player.center()
        if self.progress_bar is not None:
            self.progress_bar.update()
            self.progress_bar.draw()

    def clean_up_states(self):
        self.system.clean_up_states([
            self.player.speed_state.state,
            self.player.move_state.state,
            self.player.power_state.state,
            self.player.life_state.state,
            self.session.state.state
            ])
        if self.tutorial_state is not None:
            self.system.clean_up_states([self.tutorial_state.state])

    def register_debug_telemetry(self):
        self.system.app_inspector["daytime"] = self.environment.day_cycle.get_daytime()
        self.system.app_inspector["brightness"] = self.environment.day_cycle.get_brightness()
        self.system.app_inspector["temperature"] = self.environment.temperature.get_temperature()
        if self.player:
            self.system.app_inspector["shrinkrate"] = self.player.shrink_rate
            
            snl = self.debug.draw_debug_snowflake_lines
            rkl = self.debug.draw_debug_rock_lines
            pul = self.debug.draw_debug_powerup_lines
            rel = self.debug.draw_debug_reducer_lines
            
            self.system.app_inspector["snowflk_tracers"] =  snl if snl is not False else None
            self.system.app_inspector["rock_tracers"] =  rkl if rkl is not False else None
            self.system.app_inspector["powerup_tracers"] =  pul if pul is not False else None
            self.system.app_inspector["reducer_tracers"] =  rel if rel is not False else None

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