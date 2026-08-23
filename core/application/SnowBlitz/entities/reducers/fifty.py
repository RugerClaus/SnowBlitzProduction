from core.application.SnowBlitz.entities.reducers.levelreducer import LevelReducer
from core.application.SnowBlitz.entities.reducers.type import LRType

class Fifty(LevelReducer):
    def __init__(self, board_surface,camera=None):
        super().__init__(board_surface, LRType.FIFTY,camera)

    def get_reducer_number(self):
        return 50