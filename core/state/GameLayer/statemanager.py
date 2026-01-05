from helper import log_state_transition
from core.state.GameLayer.state import GAMESTATE
from core.state.basestatemanager import BaseStateManager

class GameStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            GAMESTATE.PLAYING: [GAMESTATE.PAUSED, GAMESTATE.GAME_OVER],
            GAMESTATE.PAUSED: [GAMESTATE.PLAYING],
            GAMESTATE.GAME_OVER: [GAMESTATE.PLAYING]
        }
        super().__init__(
            initial_state=GAMESTATE.PLAYING,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type, 'game'),
            state_name="GAMESTATE"
        )
