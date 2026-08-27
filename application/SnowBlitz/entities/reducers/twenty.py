from application.SnowBlitz.entities.reducers.levelreducer import LevelReducer
from application.SnowBlitz.entities.reducers.type import LRType

class Twenty(LevelReducer):
    def __init__(self, board_surface,camera=None):
        super().__init__(board_surface, LRType.TWENTY,camera)
    
    def get_reducer_number(self):
        return 20