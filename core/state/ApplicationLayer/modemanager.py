from core.state.ApplicationLayer.mode import APPMODE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class ModeManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            APPMODE.PRIMARY: [APPMODE.DEBUG],
            APPMODE.DEBUG: [APPMODE.PRIMARY]
        }

        super().__init__(
                initial_state=APPMODE.PRIMARY,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="APPMODE"
            )
