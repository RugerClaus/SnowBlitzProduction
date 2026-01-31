from helper import log_state_transition
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.state.basestatemanager import BaseStateManager

class GameModeManager(BaseStateManager):
    def __init__(self, initial_state=GAME_MODE.NONE):
        allowed_transitions = {
            GAME_MODE.NONE: [
                GAME_MODE.ENDLESS,
                GAME_MODE.BLITZ,
                GAME_MODE.TUTORIAL
            ],
            GAME_MODE.ENDLESS: [
                GAME_MODE.NONE
            ],
            GAME_MODE.BLITZ: [
                GAME_MODE.NONE
            ],
            GAME_MODE.TUTORIAL: [
                GAME_MODE.NONE
            ]
        }
        super().__init__(
            initial_state=initial_state,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="GAMEMODE"
        )
