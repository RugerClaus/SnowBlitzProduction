from core.state.basestatemanager import BaseStateManager
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from helper import log_state_transition

class PlayerSpeedStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_INTENT_STATE.IDLE_TURN):
        allowed_transitions = {
            PLAYER_INTENT_STATE.WALK: [
                PLAYER_INTENT_STATE.SPRINT
            ],
            PLAYER_INTENT_STATE.SPRINT: [
                PLAYER_INTENT_STATE.WALK
            ],
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="SPEEDSTATE"
        )
