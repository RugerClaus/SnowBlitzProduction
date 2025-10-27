from core.state.ApplicationLayer.state import APPSTATE
from helper import log_system_state_transitions

class StateManager:
    def __init__(self):
        #app states
        self.app_state = APPSTATE.MAIN_MENU
        self.previous_app_state = None

        #allowed transition definitions
        self.app_allowed_transitions = {
            APPSTATE.MAIN_MENU: [APPSTATE.IN_GAME,APPSTATE.LOAD_MENU,APPSTATE.QUIT],
            APPSTATE.LOAD_MENU: [APPSTATE.MAIN_MENU,APPSTATE.IN_GAME,APPSTATE.QUIT],
            APPSTATE.IN_GAME: [APPSTATE.MAIN_MENU,APPSTATE.QUIT]
        }
    
    def set_app_state(self,new_state):
        if new_state == self.app_state:
            return
        if new_state in self.app_allowed_transitions.get(self.app_state,[]):
            log_system_state_transitions(self.app_state,new_state,"APPSTATE")
            self.set_previous_app_state(self.app_state)
            self.app_state = new_state
            print(self.get_app_state())

    def is_app_state(self,state):
        return self.app_state == state
    
    def get_app_state(self):
        return f"Appstate: {self.app_state}"
    
    def set_previous_app_state(self,state):
        self.previous_app_state = state