
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
class PlayerMechanics:
    @staticmethod
    def update_movement(move_state, speed, x):
        if move_state.is_state(PLAYER_INTENT_STATE.MOVE_LEFT):
            x -= speed
        elif move_state.is_state(PLAYER_INTENT_STATE.MOVE_RIGHT):
             x += speed
        elif move_state.is_state(PLAYER_INTENT_STATE.IDLE_MOVE):
            speed += 0
        return x
    
    @staticmethod
    def check_death(diam, life_state, move_state):
        if diam < 1:
            life_state.set_state(PLAYER_LIFE_STATE.DEAD)
            move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)

    @staticmethod
    def calculate_shrink_rate(diam):
        if diam >= 350:
            shrink_rate = 1
        elif diam >= 325:
            shrink_rate = 0.9
        elif diam >= 300:
            shrink_rate = 0.8
        elif diam >= 275:
            shrink_rate = 0.7
        elif diam >= 250:
            shrink_rate = 0.6
        elif diam >= 225:
            shrink_rate = 0.5
        elif diam >= 200:
            shrink_rate = 0.4
        elif diam >= 175:
            shrink_rate = 0.3
        elif diam >= 150:
            shrink_rate = 0.2
        elif diam >= 125:
            shrink_rate = 0.1
        elif diam >= 100:
            shrink_rate = 0.09
        elif diam >= 75:
            shrink_rate = 0.08
        elif diam >= 50:
            shrink_rate = 0.07
        elif diam >= 40:
            shrink_rate = 0.05
        elif diam >= 10:
            shrink_rate = 0.02
        else:
            shrink_rate = 0.01
        return shrink_rate