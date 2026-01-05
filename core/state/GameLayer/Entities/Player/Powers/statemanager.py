from helper import log_state_transition
from core.state.GameLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerPowerStateManager(BaseStateManager):
    def __init__(self, initial_state=PLAYER_POWER_STATE.NONE):
        allowed_transitions = {
            PLAYER_POWER_STATE.NONE: [
                PLAYER_POWER_STATE.ABSORB_ROCK,
                PLAYER_POWER_STATE.ANTI_SHRINK,
                PLAYER_POWER_STATE.GROW_SLOW
            ],
            PLAYER_POWER_STATE.ABSORB_ROCK: [
                PLAYER_POWER_STATE.ANTI_SHRINK,
                PLAYER_POWER_STATE.GROW_SLOW,
                PLAYER_POWER_STATE.NONE
            ],
            PLAYER_POWER_STATE.ANTI_SHRINK: [
                PLAYER_POWER_STATE.ABSORB_ROCK,
                PLAYER_POWER_STATE.GROW_SLOW,
                PLAYER_POWER_STATE.NONE
            ],
            PLAYER_POWER_STATE.GROW_SLOW: [
                PLAYER_POWER_STATE.ABSORB_ROCK,
                PLAYER_POWER_STATE.ANTI_SHRINK,
                PLAYER_POWER_STATE.NONE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type, 'game/player'),
            state_name="PLAYERPOWERSTATE"
        )
