from core.game.entities.EntityState.state import *
from core.game.entities.EntityState.transitions import player_states as ps

class EntityStateManager:
    def __init__(self):
        #player intent states
        self.player_intent_state = PLAYER_INTENT_STATE.IDLE
        self.previous_player_intent_state = None
        
        #player movement states

        #allowed transition definitions
        self.player_intent_state_allowed_transitions = ps
    
    def set_player_intent_state(self,new_state):
        if new_state == self.player_intent_state:
            return
        if new_state in self.player_intent_state_allowed_transitions.get(self.player_intent_state,[]):
            self.set_previous_app_state(self.previous_player_intent_state)
            self.player_intent_state = new_state
            print(self.get_player_intent_state())

    def is_player_intent_state(self,state):
        return self.player_intent_state == state
    
    def get_player_intent_state(self):
        return f"Appstate: {self.player_intent_state}"
    
    def set_previous_player_intent_state(self,state):
        self.previous_app_state = state
