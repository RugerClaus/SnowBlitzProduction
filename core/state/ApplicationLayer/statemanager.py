from core.state.ApplicationLayer.state import APPSTATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class StateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            APPSTATE.MAIN_MENU: [APPSTATE.IN_GAME,APPSTATE.QUIT],
            APPSTATE.IN_GAME: [APPSTATE.MAIN_MENU,APPSTATE.QUIT]
        }
        
        super().__init__(
                initial_state=APPSTATE.MAIN_MENU,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="APPSTATE"
            )
