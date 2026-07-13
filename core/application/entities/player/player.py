from core.application.entities.type import EntityType
from core.application.entities.entity import Entity

from core.state.ApplicationLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.ApplicationLayer.Entities.Player.Speed.state import SPEED_STATE

from core.state.ApplicationLayer.Entities.Player.Speed.statemanager import SpeedStateManager
from core.state.ApplicationLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.ApplicationLayer.Entities.Player.Powers.statemanager import PlayerPowerStateManager
from core.state.ApplicationLayer.Entities.Player.Life.statemanager import PlayerLifeStateManager

from core.application.entities.player.playermechanics import PlayerMechanics as physics
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE


class Player(Entity):

    def __init__(self, system, entitymanager, game_state, environment, session):

        self.system = system
        self.entitymanager = entitymanager
        self.game_state = game_state
        self.environment = environment
        self.session = session

        self.user = system.user

        self.x_ratio = 0.5
        self.y_ratio = 0.90

        # normalized size relative to screen height
        self.diam_ratio = 0.015

        # calculated pixel diameter
        self.diam = self.get_pixel_diameter()

        self.base_size = self.diam / 2


        super().__init__(
            self.x_ratio,
            self.y_ratio,
            self.system.window,
            EntityType.PLAYER,
            self.diam
        )


        self.life_state = PlayerLifeStateManager()
        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()
        self.speed_state = SpeedStateManager()


        self.powerup_duration = 5000
        self.last_powerup_start_time = None

        self.shrink_rate = None

        self.reset()



    def get_pixel_diameter(self):

        return max(
            6,
            int(
                self.system.window.get_height()
                *
                self.diam_ratio
            )
        )



    def rebuild_surface(self):

        visual_size = max(
            5,
            int(self.render_diam)
        )

        self.base_size = visual_size / 2

        self.surface = self.system.window.make_surface(
            visual_size,
            visual_size,
            True
        )

        self.rect = self.surface.get_rect()

        self.update_position_from_ratio()



    def update_position_from_ratio(self):

        self.x = (
            self.system.window.get_width()
            *
            self.x_ratio
        )

        self.y = (
            self.system.window.get_height()
            *
            self.y_ratio
        )


        self.rect.centerx = int(self.x)
        self.rect.bottom = int(self.y)



    def scale(self):

        self.rebuild_surface()



    def center(self):

        self.x_ratio = 0.5

        self.update_position_from_ratio()



    def update(self):

        physics.check_collisions(
            self.entitymanager.get_active_entities(),
            self
        )


        physics.check_high_score(self)


        self.powerup_duration = (
            physics.calculate_powerup_duration(
                self.score
            )
        )


        if self.system.control_state.is_state(
            DEVELOPER_MODE.ON
        ):

            self.shrink_rate = 0

        else:

            self.shrink_rate = (
                physics.calculate_shrink_rate(
                    self.diam,
                    self,
                    self.environment
                )
            )

        self.diam -= self.shrink_rate

        self.diam = max(
            self.diam,
            1
        )

        # smooth visual transition
        self.render_diam += (
            self.diam - self.render_diam
        ) * 0.1

        self.rebuild_surface()

        if self.system.control_state.is_state(DEVELOPER_MODE.OFF):
            self.score += int(
                1.1 * self.multiplier
            )
        physics.update_multiplier(self)

        self.speed = physics.update_speed(
            self.speed_state
        )


        movement = physics.update_movement(
            self.move_state,
            self.speed
        )


        self.x_ratio += (
            movement
            /
            self.system.window.get_width()
        )



        physics.check_size_death(
            self.diam,
            self.life_state,
            self.move_state
        )


        physics.check_level_up(
            self,
            self.entitymanager
        )


        physics.check_power_state(
            self
        )


        physics.handle_powerup_timer(
            self
        )


        physics.handle_sfx(
            self
        )


        physics.check_death(
            self,
            self.game_state,
            self.session,
            self.system
        )


        physics.check_bounds(
            self
        )


        self.update_position_from_ratio()



    def move(self, direction):

        if direction == "LEFT":

            self.move_state.set_state(
                PLAYER_INTENT_STATE.MOVE_LEFT
            )

            self.speed_state.set_state(
                SPEED_STATE.NORMAL
            )


        elif direction == "RIGHT":

            self.move_state.set_state(
                PLAYER_INTENT_STATE.MOVE_RIGHT
            )

            self.speed_state.set_state(
                SPEED_STATE.NORMAL
            )


        elif direction == "NONE":

            self.move_state.set_state(
                PLAYER_INTENT_STATE.IDLE
            )

            self.speed_state.set_state(
                SPEED_STATE.NORMAL
            )


        elif direction == "SLOW_LEFT":

            self.move_state.set_state(
                PLAYER_INTENT_STATE.MOVE_LEFT
            )

            self.speed_state.set_state(
                SPEED_STATE.SLOW
            )


        elif direction == "SLOW_RIGHT":

            self.move_state.set_state(
                PLAYER_INTENT_STATE.MOVE_RIGHT
            )

            self.speed_state.set_state(
                SPEED_STATE.SLOW
            )



    def draw(self):

        self.surface.fill(
            (0, 0, 0, 0)
        )


        self.system.window.draw_circle(
            self.surface,
            self.color,
            (
                self.base_size,
                self.base_size
            ),
            self.base_size,
            self.type
        )


        self.system.window.blit(
            self.surface,
            self.rect.topleft
        )



    def draw_wait(self):

        self.draw()



    def reset(self):

        self.original_height = (
            self.system.window.get_height()
        )

        # gameplay diameter
        self.diam = (
            self.system.window.get_height()
            *
            self.diam_ratio
        )

        self.diam = max(
            self.diam,
            6
        )

        # visual diameter follows gameplay diameter smoothly
        self.render_diam = self.diam


        self.x_ratio = 0.5
        self.y_ratio = 0.90


        self.speed = 7


        self.color = (
            255,
            255,
            255
        )


        self.multiplier = 1

        self.user = self.system.user


        self.score = 0

        self.current_level = 1


        self.level_up_size = (
            physics.calculate_level_up_size(
                self.current_level
            )
        )


        self.life_state = PlayerLifeStateManager()
        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()
        self.speed_state = SpeedStateManager()


        self.current_high_score = (
            physics.get_current_high_score(
                self.user
            )
        )


        physics.reset_states(
            self
        )


        self.last_powerup_start_time = None
        self.powerup_duration = 5000
        self.shrink_rate = None


        self.rebuild_surface()

        self.update_position_from_ratio()