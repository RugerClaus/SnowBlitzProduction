
from core.game.entities.state.statemanager import EntityStateManager
class Entities:
    def __init__(self):
        self.state = EntityStateManager()
        self.players = []

        self.neutral_mobs = []
        self.hostile_mobs = []
        self.friendly_mobs = []
        
        self.health_potions = []

        self.interactive_tiles = []
