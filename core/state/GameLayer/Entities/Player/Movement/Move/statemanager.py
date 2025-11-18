from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerMoveStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_INTENT_STATE.IDLE_MOVE):
        allowed_transitions = {
            PLAYER_INTENT_STATE.IDLE_MOVE: [
                PLAYER_INTENT_STATE.MOVE_FORWARD,
                PLAYER_INTENT_STATE.MOVE_BACKWARD
            ],
            PLAYER_INTENT_STATE.MOVE_FORWARD: [
                PLAYER_INTENT_STATE.MOVE_BACKWARD,
                PLAYER_INTENT_STATE.IDLE_MOVE
            ],
            PLAYER_INTENT_STATE.MOVE_BACKWARD: [
                PLAYER_INTENT_STATE.MOVE_FORWARD,
                PLAYER_INTENT_STATE.IDLE_MOVE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="MOVESTATE"
        )
