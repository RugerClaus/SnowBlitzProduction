from enum import Enum, auto

class EDITOR_MODE_LAYER_STATE(Enum):
    IDLE = auto()
    DRAW_MODE = auto()
    ERASE_MODE = auto()
    SELECT_MODE = auto()