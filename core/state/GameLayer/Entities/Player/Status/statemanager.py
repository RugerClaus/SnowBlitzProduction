from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Status.state import PLAYER_STATUS_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerStatusStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_STATUS_STATE.NORMAL):
        allowed_transitions = {
            PLAYER_STATUS_STATE.NORMAL: [
                PLAYER_STATUS_STATE.POWERUP,
            ],
            PLAYER_STATUS_STATE.POWERUP: [
                PLAYER_STATUS_STATE.NORMAL,
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="PLAYERSTATUSSTATE"
        )
