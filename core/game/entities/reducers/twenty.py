from core.game.entities.reducers.levelreducer import LevelReducer
from core.game.entities.reducers.type import LRType

class Twenty(LevelReducer):
    def __init__(self, board_surface):
        super().__init__(board_surface, LRType.TWENTY)
    
    def get_reducer_number(self):
        return 20