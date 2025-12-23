from core.state.GameLayer.state import GAMESTATE

class Endless:
    def __init__(self,surface,player,game_state):
        self.surface = surface
        self.player = player
        self.game_state = game_state

    def run(self):
        if not self.player.is_alive():
            self.game_state.set_state(GAMESTATE.GAME_OVER)
            return
        self.player.update()
        self.player.draw()