from core.state.ApplicationLayer.Game.statemanager import GameStateManager
from core.state.ApplicationLayer.GameMode.statemanager import GameModeManager
from core.state.ApplicationLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.ApplicationLayer.Game.state import GAMESTATE
from core.state.ApplicationLayer.GameMode.state import GAME_MODE
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE

from core.application.SnowBlitz.entities.entitymanager import EntityManager
from core.application.SnowBlitz.modes.endless import Endless
from core.application.SnowBlitz.modes.tutorial.tutorial import Tutorial
from core.application.SnowBlitz.modes.tutorial.tutorialmanager import TutorialManager
from core.application.SnowBlitz.modes.tutorial.prompts import Prompts
from core.application.SnowBlitz.entities.player.player import Player
from core.application.SnowBlitz.entities.player.ui.uimanager import PlayerUIManager

from core.application.SnowBlitz.debug.sbdebugutils import SBDebugUtils

from core.application.SnowBlitz.timer import GameTimer

from core.application.SnowBlitz.entities.sun.sun import Sun
from core.engine.world.mechanics.environment.environment import Environment
from core.engine.world.mechanics.effects.particles import Particles
from core.application.world.world import World

class SnowBlitz:
    def __init__(self,application):
        self.application = application
        self.disant_realms = application.distant_realms
        self.system = self.application.system
        self.session = self.application.session
        self.mode = GameModeManager()
        self.state = GameStateManager()
        
        self.environment = Environment(self.system)
        self.sun = Sun(self.system,self.environment.day_cycle)
        self.world = World(self.system,self.environment)
        self.entitymanager = EntityManager(self.system,self.world.camera)
        self.debug = SBDebugUtils(self.system,self)
        
        self.endless = None
        self.tutorial = None
        self.blitz = None
        self.start_time = self.system.time.get_current_time()
        self.player = None
        self.hud = None
        self.endless = None
        self.tutorial_manager = None
        self.prompts = None
        self.tutorial_state = None
        self.timer = None   
        self.water_particles = None

    def scale(self):
        if self.player is not None:
            self.player.scale()
            self.player.center()
        if self.hud is not None:
            self.hud.scale()

        if self.world:
            self.world.scale()

    def handle_event(self,event,command=None):
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
            if self.water_particles:
                self.water_particles.handle_event(event,command)
        else:
            pass

        if not self.mode.is_state(GAME_MODE.NONE):
            if event.type == self.system.input.keydown():
                if event.key == self.system.input.keys.escape_key():
                    self.toggle_pause()
            if self.state.is_state(GAMESTATE.PLAYING):
                if event.type == self.system.input.window_focus_lost():
                    self.toggle_pause()

        if not self.state.is_state(GAMESTATE.NONE):
            self.debug.handle_event(event,command)

    def update(self):
        
        if self.state.is_state(GAMESTATE.PLAYING):
            self.timer.update()
            self.session.update()
            self.environment.update()
            self.sun.update()

            if self.hud:
                self.hud.update()

            if self.water_particles:
                self.water_particles.update()

            if self.mode.is_state(GAME_MODE.ENDLESS):
                self.init_endless()
                self.endless.update()
            elif self.mode.is_state(GAME_MODE.TUTORIAL):
                self.init_tutorial()
                self.tutorial.update()
            elif self.mode.is_state(GAME_MODE.BLITZ):
                if self.blitz is None:
                    pass
                self.blitz.update()
            self.debug.update()

            if self.world:
                self.world.update()
        self.application.ui_util.update_audio()
        

    def draw(self):
        self.environment.draw()
        self.sun.draw()
        if self.world:
            self.world.draw()

        if self.hud:
            self.hud.draw()
        if self.water_particles:
            self.water_particles.draw()

        if self.mode.is_state(GAME_MODE.ENDLESS):
            
            self.endless.draw()
            self.handle_debug_state()
        elif self.mode.is_state(GAME_MODE.TUTORIAL):
            
            self.tutorial.draw()
            self.handle_debug_state()
        elif self.mode.is_state(GAME_MODE.BLITZ):
            if self.blitz is None:
                pass
            self.blitz.draw()

    def toggle_pause(self):
        if self.state.is_state(GAMESTATE.PLAYING):
            self.state.set_state(GAMESTATE.PAUSED)
            self.disant_realms.ui_controller.show_ui("pause")
        elif self.state.is_state(GAMESTATE.PAUSED):
            self.environment.day_cycle.resume()
            self.timer.resume()
            self.state.set_state(GAMESTATE.PLAYING)
            self.disant_realms.ui_controller.clear()

    def toggle_hud(self):
        if self.hud is not None:
            self.hud.toggle()

    def init_player(self):
        if self.player is None:
            self.player = Player(self.system,self.entitymanager,self.state,self.environment,self.session,self.timer)
            self.world.camera.follow(self.player)

        if self.hud is None:
            self.hud = PlayerUIManager(self.system,self.player)

        if self.water_particles is None:
            self.water_particles = Particles(self.system,self.player)

    def init_game(self,game_mode):
        self.reset()
        self.state.set_state(GAMESTATE.PLAYING)
        self.timer = GameTimer(self.system)

        if game_mode == "endless":
            self.mode.set_state(GAME_MODE.ENDLESS)
            self.disant_realms.ui_controller.clear()
            self.init_endless()

        elif game_mode == "tutorial":
            self.mode.set_state(GAME_MODE.TUTORIAL)
            self.disant_realms.ui_controller.clear()
            self.init_tutorial()

    def init_endless(self):
            if not self.application.session_started:
                self.application.session_started = True
                self.session.start_online_session()
    
            self.init_player()

            if self.endless is None:
                self.endless = Endless(
                    self.hud,
                    self.player,
                    self.entitymanager
                )

    def init_tutorial(self):
        self.init_player()
        if self.prompts is None:
            self.prompts = Prompts(self.system.window,self.player,self.system.input)
        if self.tutorial_state is None:
            self.tutorial_state = TutorialStateManager()
        if self.tutorial_manager is None: 
            self.tutorial_manager = TutorialManager(self.system, self.prompts,self.system.input.game_controls,
                                                self.entitymanager,self.player,self.hud,self.tutorial_state)
        if self.tutorial is None:
            self.tutorial = Tutorial(self.system.window,self.player,self.entitymanager,self.system.input.game_controls,
                                                self.hud,self.tutorial_state,self.tutorial_manager,self.prompts)

    def handle_debug_state(self):
        self.debug.draw()
        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            if self.session.state.is_state(ONLINE_SESSION_STATE.ACTIVE):
                self.session.end_online_session()

    def reset_systems(self):
        if self.mode.is_state(GAME_MODE.TUTORIAL):
            self.system.user.high_score = 0
        del self.player
        del self.hud
        del self.endless
        del self.tutorial
        del self.tutorial_state
        del self.tutorial_manager
        del self.prompts
        del self.blitz
        self.player = None
        self.hud = None
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

        if self.hud is not None:
            self.hud.reset_timer()
            self.hud.draw()

        self.entitymanager.reset_entities()
        self.entitymanager.reset_spawn_timers()

    def clean_up_states(self):
        self.system.clean_up_states([
            self.mode.state,
            self.state.state,
            self.environment.season.state.state,
        ])
        self.player.clean_up_states()
        if self.tutorial_state is not None:
            self.system.clean_up_states([self.tutorial_state.state])