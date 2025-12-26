from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.GameLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.GameLayer.state import GAMESTATE

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
    
    def check_bounds(player):
        if player.x <= 5:
            player.x = 5
        elif player.x >= player.board_surface.get_width() - 5:
            player.x = player.board_surface.get_width() - 5
    
    @staticmethod
    def check_size_death(diam, life_state, move_state):
        if diam == 0:

            life_state.set_state(PLAYER_LIFE_STATE.DEAD)
            move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)
            return True  # Indicating death occurred
        return False

    def check_death(player,game_state):
        if player.life_state.is_state(PLAYER_LIFE_STATE.DEAD):
            game_state.set_state(GAMESTATE.GAME_OVER)
        else:
            return

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

    @staticmethod
    def check_level_up(player,entitymanager):
        if player.diam >= player.level_up_size:
            player.level_up_size = PlayerMechanics.calculate_level_up_size(player.level_up_size // 10)
            print(player.level_up_size)
            player.current_level += 1
            player.diam = 10
            player.base_size = player.diam / 2 
            entitymanager.reset_entities()
            print(player.current_level)
            return True
        return False
    
    @staticmethod
    def calculate_level_up_size(current_level):
        return 10 + (current_level) * 10
    
    @staticmethod
    def resize(player):
        bottom = player.rect.bottom  # save ground position
        player.surface = player.board_surface.make_surface(player.diam, player.diam, True)
        player.rect = player.surface.get_rect()
        player.rect.bottom = bottom
        player.rect.centerx = int(player.x)

    @staticmethod
    def collect_snowflake(player,snowflake):
        player.diam += snowflake.diam // 2
        print("collected")

    @staticmethod
    def handle_rock(player,rock):
        if not player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
            player.life_state.set_state(PLAYER_LIFE_STATE.DEAD)
        else:
            player.diam += rock.diam / 4 #gain 1/4 of the rock's diameter