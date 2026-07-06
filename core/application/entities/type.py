from enum import Enum, auto

class EntityType(Enum):
    PLAYER = auto()
    POWERUP = auto()
    SNOWFLAKE = auto()
    ROCK = auto()
    REDUCER = auto()
    SUN = auto()