from core.state.TileMapEditorLayer.state import TILE_EDITOR_MASTER_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class TileEditorMasterStateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            TILE_EDITOR_MASTER_STATE.ACTIVE: [TILE_EDITOR_MASTER_STATE.PAUSED],
            TILE_EDITOR_MASTER_STATE.PAUSED: [TILE_EDITOR_MASTER_STATE.ACTIVE]
        }
        super().__init__(
            initial_state=TILE_EDITOR_MASTER_STATE.ACTIVE,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="TILE_EDITOR_MASTER_STATE"
        )
