
from core.application.network.sessions import Session
from core.state.ApplicationLayer.Game.state import GAMESTATE
from core.state.ApplicationLayer.Game.statemanager import GameStateManager
from core.application.SnowBlitz.snowblitz import SnowBlitz


class Application:
    def __init__(self,distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system
        self.game_state = GameStateManager()
        self.session = Session(self.system)
        self.session_started = False 

        self.snow_blitz = SnowBlitz(self)

        self.clean_up_states()

    

    def handle_event(self, event, command=None):
        if self.snow_blitz:
            self.snow_blitz.handle_event(event,command)
    
    def update(self):
        if not self.game_state.is_state(GAMESTATE.NONE):
            if self.snow_blitz and self.game_state.is_state(GAMESTATE.PLAYING):
                self.snow_blitz.update()

    def draw(self):
        if self.snow_blitz:
            self.snow_blitz.draw()
            
    def scale(self):
        if self.snow_blitz:
            self.snow_blitz.scale()
            

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
        if self.snow_blitz:
            self.snow_blitz.register_debug_telemetry()
            
    def reset(self):
        if self.snow_blitz:
            self.snow_blitz.reset()
            self.snow_blitz.reset_systems()


    def clean_up_states(self):
        self.system.clean_up_states([
            self.game_state.state,
        ])
        self.snow_blitz.clean_up_states()
        self.session.clean_up_states()