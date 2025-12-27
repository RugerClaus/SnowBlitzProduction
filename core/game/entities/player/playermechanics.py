from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.GameLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.GameLayer.state import GAMESTATE
from core.game.entities.powerups.type import PowerUpType

class PlayerMechanics:
    @staticmethod
    def update_movement(move_state, speed, x):
        acceleration = 0.05
        if move_state.is_state(PLAYER_INTENT_STATE.MOVE_LEFT):
            speed -= acceleration
            x -= speed
        elif move_state.is_state(PLAYER_INTENT_STATE.MOVE_RIGHT):
            speed += acceleration
            x += speed
        elif move_state.is_state(PLAYER_INTENT_STATE.IDLE_MOVE):
            acceleration = 0
            x += 0
        return x
    
    def check_bounds(player):
        if player.x <= 5:
            player.x = 5
        elif player.x >= player.board_surface.get_width() - 5:
            player.x = player.board_surface.get_width() - 5
    
    @staticmethod
    def check_size_death(diam, life_state, move_state):
        if diam < 3:

            life_state.set_state(PLAYER_LIFE_STATE.DEAD)
            move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)
            return True  # Indicating death occurred
        return False

    def check_death(player,game_state):
        if player.life_state.is_state(PLAYER_LIFE_STATE.DEAD):
            game_state.set_state(GAMESTATE.GAME_OVER)
        else:
            return

    def check_power_state(player):
        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
                player.color = (0,0,255)
            elif player.power_state.is_state(PLAYER_POWER_STATE.ANTI_SHRINK):
                player.color = (0,255,0)
        else:
            player.color = (255,255,255)
        
    @staticmethod
    def calculate_shrink_rate(diam,player):

        if player.power_state.is_state(PLAYER_POWER_STATE.ANTI_SHRINK) or player.shrink_rate == 0:
            return 0
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
            player.level_up_size = PlayerMechanics.calculate_level_up_size(player.current_level)
            player.current_level += 1
            player.diam = 10
            player.base_size = player.diam / 2 
            entitymanager.reset_entities()
            player.power_state.set_state(PLAYER_POWER_STATE.NONE)
            return True
        return False
    
    @staticmethod
    def calculate_level_up_size(current_level):
        return 10 + (current_level) * 5

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

    @staticmethod
    def handle_rock(player,rock):
        if not player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
            player.life_state.set_state(PLAYER_LIFE_STATE.DEAD)
        else:
            player.diam += rock.width / 4 #gain 1/4 of the rock's width
    
    def calculate_powerup_duration(score):
        # Check score ranges and return the corresponding duration, otherwise return a default duration
        if score >= 100000:
            return 7500
        elif score >= 50000:
            return 6870
        elif score >= 20000:
            return 6500
        elif score >= 10000:
            return 6000
        else:
            return 5000

    @staticmethod
    def find_powerup_type(player,powerup):
        if powerup.power_type == PowerUpType.ABSORB_ROCK:
            player.power_state.set_state(PLAYER_POWER_STATE.ABSORB_ROCK)
        elif powerup.power_type == PowerUpType.ANTI_SHRINK:
            player.power_state.set_state(PLAYER_POWER_STATE.ANTI_SHRINK)

    @staticmethod
    def handle_powerup(player, powerup):
        PlayerMechanics.find_powerup_type(player, powerup)
        player.color = powerup.color

        if player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
            
            if player.last_powerup_start_time is None:
                player.last_powerup_start_time = player.board_surface.get_current_time()

        elif player.power_state.is_state(PLAYER_POWER_STATE.ANTI_SHRINK):
            if player.last_powerup_start_time is None: 
                player.last_powerup_start_time = player.board_surface.get_current_time()
                player.shrink_rate = 0


    @staticmethod
    def handle_powerup_timer(player):
        # If the player has an active powerup
        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if player.last_powerup_start_time:
                current_time = player.board_surface.get_current_time()
                
                # Check if the powerup time has elapsed
                if current_time - player.last_powerup_start_time > player.powerup_duration:
                    
                    player.color = (255, 255, 255)
                    player.power_state.set_state(PLAYER_POWER_STATE.NONE)
                    player.last_powerup_start_time = None
                    player.shrink_rate = PlayerMechanics.calculate_shrink_rate(player.diam,player)
    
    @staticmethod
    def apply_powerup(player, new_power_state, duration):
        player.power_state.set_state(new_power_state)
        player.powerup_duration = duration
        
        # Reset the timer
        player.last_powerup_start_time = player.board_surface.get_current_time()
            

    @staticmethod
    def handle_reducer(player,reducer):
        number = reducer.get_reducer_number()
        player.level_up_size -= number if number < player.level_up_size else player.level_up_size - 1


    @staticmethod
    def handle_sfx(player):

        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if 'powerup_active' not in player.sound.active_sfx: 
                player.sound.play_sfx('powerup_active')
        else:
            if 'powerup_active' in player.sound.active_sfx:
                player.sound.stop_sfx('powerup_active')

    @staticmethod
    def reset_states(player):
        player.life_state.set_state(PLAYER_LIFE_STATE.ALIVE)
        player.move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)
        player.power_state.set_state(PLAYER_POWER_STATE.NONE)