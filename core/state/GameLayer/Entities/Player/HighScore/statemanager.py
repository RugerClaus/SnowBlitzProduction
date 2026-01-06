from helper import log_state_transition
from core.state.GameLayer.Entities.Player.HighScore.state import HIGH_SCORE_STATE
from core.state.basestatemanager import BaseStateManager

class PlayerHighScoreStateManager(BaseStateManager):
    def __init__(self, initial_state=HIGH_SCORE_STATE.NONE):
        allowed_transitions = {
            HIGH_SCORE_STATE.BROKEN: [
                HIGH_SCORE_STATE.NONE
            ],
            HIGH_SCORE_STATE.NONE: [
                HIGH_SCORE_STATE.BROKEN
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type, 'game/player'),
            state_name="PLAYERHIGHSCORESTATE"
        )
