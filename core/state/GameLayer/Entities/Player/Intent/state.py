from enum import Enum,auto

class PLAYER_INTENT_STATE(Enum):
    MOVE_FORWARD = auto()
    MOVE_BACKWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    IDLE_MOVE = auto()
    IDLE_TURN = auto()