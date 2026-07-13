from core.state.ApplicationLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.ApplicationLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.ApplicationLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.ApplicationLayer.Entities.Player.Speed.state import SPEED_STATE
from core.state.ApplicationLayer.state import GAMESTATE
from core.application.entities.powerups.type import PowerUpType
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.application.entities.type import EntityType

class PlayerMechanics:

    @staticmethod
    @staticmethod
    def get_current_high_score(user):
        return user.high_score

    @staticmethod
    def update_speed(speed_state):
        if speed_state.is_state(SPEED_STATE.NORMAL):
            return 7
        elif speed_state.is_state(SPEED_STATE.SLOW):
            return 4
        elif speed_state.is_state(SPEED_STATE.FAST):
            return 10


    @staticmethod
    def update_movement(move_state, speed):
        acceleration = 1

        if move_state.is_state(PLAYER_INTENT_STATE.MOVE_LEFT):
            return -(speed * acceleration)

        elif move_state.is_state(PLAYER_INTENT_STATE.MOVE_RIGHT):
            return speed * acceleration

        return 0
    @staticmethod
    def check_bounds(player):
        if player.x <= 5:
            player.x = 5
        elif player.x >= player.board_surface.get_width() - 5:
            player.x = player.board_surface.get_width() - 5
    
    @staticmethod
    def check_death(player, game_state, game_session, system):
        if player.life_state.is_state(PLAYER_LIFE_STATE.DEAD):
            game_state.set_state(GAMESTATE.GAME_OVER)

            if system.control_state.is_state(DEVELOPER_MODE.OFF):

                stored = system.load.read_constant("high_score")
                stored = int(stored) if stored else 0

                if player.score > stored:
                    system.save.write_constant(
                        "high_score",
                        str(player.score)
                    )
            game_session.submit_score(player.score)

            
    @staticmethod
    def check_high_score(player):
        stored = player.system.load.read_constant('high_score')
        stored = int(stored) if stored else 0
        if player.score >= int(stored):
                player.current_high_score = player.score
  
    @staticmethod
    def check_power_state(player):
        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
                player.color = (0,0,255)
            elif player.power_state.is_state(PLAYER_POWER_STATE.ANTI_SHRINK):
                player.color = (0,255,0)
            elif player.power_state.is_state(PLAYER_POWER_STATE.SPEED_BOOST):
                player.color = (150,150,150)
                player.speed_state.set_state(SPEED_STATE.FAST)
        else:
            player.color = (255,255,255)

    @staticmethod
    def check_collisions(entities,player):
        player_mask = player.system.window.mask(player.surface)

        for entity in entities:
            entity_mask = player.system.window.mask(entity.surface)
            offset = (entity.rect.x - player.rect.x, entity.rect.y - player.rect.y)
            if player_mask.overlap(entity_mask, offset):
                if player.system.control_state.is_state(DEVELOPER_MODE.ON):
                    return
                if entity.type == EntityType.SNOWFLAKE:
                    PlayerMechanics.collect_snowflake(player,entity)
                    player.system.sound.play_sfx('snow')
                    player.score += entity.diam
                    entity.collected()
                elif entity.type == EntityType.ROCK:
                        PlayerMechanics.handle_rock(player,entity)
                elif entity.type == EntityType.POWERUP:
                    PlayerMechanics.handle_powerup(player,entity)
                    PlayerMechanics.apply_powerup(player,entity.power_type,player.powerup_duration)
                    entity.collected()
                elif entity.type == EntityType.REDUCER:
                    PlayerMechanics.handle_reducer(player,entity)
                    entity.collected()

    @staticmethod
    def check_size_death(diam, life_state, move_state):
        if diam <= 0:
            life_state.set_state(
                PLAYER_LIFE_STATE.DEAD
            )

            move_state.set_state(
                PLAYER_INTENT_STATE.IDLE
            )

            return True

        return False


    @staticmethod
    def calculate_shrink_rate(diam, player, environment=None):

        if player.power_state.is_state(
            PLAYER_POWER_STATE.ANTI_SHRINK
        ):
            return 0
        
        if diam >= 350:
            rate = 1.0

        elif diam >= 300:
            rate = 0.8

        elif diam >= 250:
            rate = 0.6

        elif diam >= 200:
            rate = 0.4

        elif diam >= 150:
            rate = 0.2

        elif diam >= 100:
            rate = 0.09

        elif diam >= 50:
            rate = 0.05

        elif diam >= 10:
            rate = 0.02

        else:
            rate = 0.01


        if environment:

            temperature = environment.temperature.get_temperature()

            # base melting curve
            if temperature <= 20:
                rate *= 0.2

            elif temperature <= 32:
                rate *= 0.5

            elif temperature <= 50:
                rate *= 1.0

            elif temperature <= 70:
                rate *= 1.4

            elif temperature <= 85:
                rate *= 1.8

            else:
                rate *= 2.5


        return rate


    @staticmethod
    def collect_snowflake(player, snowflake):
        player.diam += snowflake.diam / 2
        print("PLAYER SIZE:", player.diam)


    @staticmethod
    def handle_rock(player, rock):

        if player.power_state.is_state(
            PLAYER_POWER_STATE.ABSORB_ROCK
        ):

            # Convert rock size into snowball growth.
            player.diam += rock.width / 4
        else:

            player.life_state.set_state(
                PLAYER_LIFE_STATE.DEAD
            )


    @staticmethod
    def check_level_up(player, entitymanager):

        if player.diam >= player.level_up_size:

            player.current_level += 1

            player.level_up_size = (
                PlayerMechanics.calculate_level_up_size(
                    player.current_level
                )
            )

            # reset snowball size after leveling
            player.diam = (
                player.system.window.get_height()
                *
                player.diam_ratio
            )

            player.diam = max(
                player.diam,
                6
            )

            # keep visual size transition smooth
            player.render_diam = player.diam

            entitymanager.reset_entities()

            player.power_state.set_state(
                PLAYER_POWER_STATE.NONE
            )

            PlayerMechanics.update_multiplier(
                player
            )

            return True

        return False
    
    @staticmethod
    def calculate_level_up_size(current_level):
        return 10 + (current_level) * 5
            
    @staticmethod
    def update_multiplier(player):
        player.multiplier = 1 + (player.current_level // 10)

    @staticmethod
    def calculate_powerup_duration(score):
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
        elif powerup.power_type == PowerUpType.SPEED_BOOST:
            player.power_state.set_state(PLAYER_POWER_STATE.SPEED_BOOST)

    @staticmethod
    def handle_powerup(player, powerup):
        PlayerMechanics.find_powerup_type(player, powerup)
        player.color = powerup.color

        if player.power_state.is_state(PLAYER_POWER_STATE.ABSORB_ROCK):
            
            if player.last_powerup_start_time is None:
                player.last_powerup_start_time = player.system.time.get_current_time()

        elif player.power_state.is_state(PLAYER_POWER_STATE.ANTI_SHRINK):
            if player.last_powerup_start_time is None: 
                player.last_powerup_start_time = player.system.time.get_current_time()
                player.shrink_rate = 0
        elif player.power_state.is_state(PLAYER_POWER_STATE.SPEED_BOOST):
            if player.last_powerup_start_time is None:
                player.last_powerup_start_time = player.system.time.get_current_time()

    @staticmethod
    def handle_powerup_timer(player):
        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if player.last_powerup_start_time:
                current_time = player.system.time.get_current_time()
                if current_time - player.last_powerup_start_time > player.powerup_duration:
                    player.color = (255, 255, 255)
                    player.power_state.set_state(PLAYER_POWER_STATE.NONE)
                    player.last_powerup_start_time = None
                    player.shrink_rate = PlayerMechanics.calculate_shrink_rate(player.diam,player)
    @staticmethod
    def map_powerup_to_state(powerup_type):
        if powerup_type == PowerUpType.ABSORB_ROCK:
            return PLAYER_POWER_STATE.ABSORB_ROCK
        elif powerup_type == PowerUpType.ANTI_SHRINK:
            return PLAYER_POWER_STATE.ANTI_SHRINK
        return None 
    
    @staticmethod
    def apply_powerup(player, new_power_state, duration):
        
        mapped_state = PlayerMechanics.map_powerup_to_state(new_power_state)

        if mapped_state:
            player.power_state.set_state(mapped_state)

        player.powerup_duration = duration
        player.last_powerup_start_time = player.system.time.get_current_time()

                

    @staticmethod
    def handle_reducer(player,reducer):
        number = reducer.get_reducer_number()
        player.level_up_size -= number if number < player.level_up_size else player.level_up_size - 1


    @staticmethod
    def handle_sfx(player):

        if not player.power_state.is_state(PLAYER_POWER_STATE.NONE):
            if 'powerup_active' not in player.system.sound.active_sfx: 
                player.system.sound.play_sfx('powerup_active')
        else:
            if 'powerup_active' in player.system.sound.active_sfx:
                player.system.sound.stop_sfx('powerup_active')

    @staticmethod
    def reset_states(player):
        player.life_state.set_state(PLAYER_LIFE_STATE.ALIVE)
        player.move_state.set_state(PLAYER_INTENT_STATE.IDLE)
        player.power_state.set_state(PLAYER_POWER_STATE.NONE)