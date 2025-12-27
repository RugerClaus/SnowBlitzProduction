from enum import Enum,auto

class TUTORIALSTATE(Enum):
    MOVEMENT_PROMPT = auto()
    BEGIN = auto()
    SNOW_PROMPT = auto()
    SNOW = auto()
    ROCKS_PROMPT = auto()
    ROCKS = auto()
    POWERUPS_PROMPT = auto()
    POWERUPS = auto()
    LEVEL_REDUCER_PROMPT = auto()
    LEVEL_REDUCERS = auto()
    WIN = auto()
    RESET = auto()