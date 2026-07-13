from systemlogging import log_state_transition
from core.state.ApplicationLayer.state import GAMESTATE
from core.state.basestatemanager import BaseStateManager

class GameStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            GAMESTATE.PLAYING: [GAMESTATE.PAUSED,GAMESTATE.NONE,GAMESTATE.GAME_OVER],
            GAMESTATE.PAUSED: [GAMESTATE.PLAYING],
            GAMESTATE.NONE: [GAMESTATE.PLAYING],
            GAMESTATE.GAME_OVER: [GAMESTATE.PLAYING,GAMESTATE.NONE]
        }
        super().__init__(
            initial_state=GAMESTATE.NONE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="GAMESTATE",
            type="APPLICATION"
        )
