
from core.game.entities.state.statemanager import EntityStateManager

class Entity():
    def __init__(self):
        self.location = ()
        self.frames = None
        self.state = EntityStateManager()
        
    def draw(self):
        pass

    def update(self):
        pass
    