from core.state.GameLayer.state import GAMESTATE
from helper import log_game_state_transitions

class GameStateManager:
    def __init__(self):
        
        #game states
        self.state = GAMESTATE.PLAYING
        self.previous_state = None
        
        #allowed transition definitions

        self.game_allowed_transitions = {
            GAMESTATE.PLAYING: [GAMESTATE.PAUSED],
            GAMESTATE.PAUSED: [GAMESTATE.PLAYING]
        }

    def set_state(self,new_state):
        if new_state == self.state:
            return
        if new_state in self.game_allowed_transitions.get(self.state,[]):
            log_game_state_transitions(self.state,new_state,"GAMESTATE")
            self.set_previous_state(self.state)
            self.state = new_state
            print(self.get_state())

    def is_state(self,state):
        return self.state == state
    
    def get_state(self):
        return f"Gamestate: {self.state}"
    
    def set_previous_state(self,state):
        self.previous_state = state
    