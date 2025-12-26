import pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Powers.statemanager import PlayerPowerStateManager
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.GameLayer.Entities.Player.Life.statemanager import PlayerLifeStateManager
from core.state.GameLayer.Entities.Player.Status.statemanager import PlayerStatusStateManager
from core.game.entities.player.playermechanics import PlayerMechanics as physics


class Player(Entity):
    def __init__(self, board_surface, entitymanager, game_state):
        self.base_size = 10
        self.x = board_surface.get_width() // 2
        self.y = board_surface.get_height() - 100
        self.entitymanager = entitymanager
        self.game_state = game_state
        super().__init__(self.x, self.y, board_surface, EntityType.PLAYER, self.base_size)
        self.reset()

        self.life_state = PlayerLifeStateManager()
        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()
        self.status_state = PlayerStatusStateManager()



    def is_alive(self):
        return self.life_state.is_state(PLAYER_LIFE_STATE.ALIVE)

    def scale(self, event_h):
        scale_factor = event_h / self.original_height
        self.base_size = 10 * scale_factor  # Scale the size of the player
        self.diam = self.diam * scale_factor
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)

        pygame.draw.circle(self.surface, (255, 255, 255), (self.base_size, self.base_size), self.base_size)

        # Keep player at a fixed position relative to screen height, but ensure the player does not go below the board_surface
        self.y = event_h - self.base_size  # Adjust y based on the new size
        if self.y + self.base_size * 2 > self.board_surface.get_height():
            self.y = self.board_surface.get_height() - self.base_size * 2  # Prevent bottom of player from going off-screen

        self.rect = self.surface.get_rect()
        self.rect.bottom = self.board_surface.get_height() - 100
        self.rect.centerx = int(self.x)

    def update(self):
        self.diam -= physics.calculate_shrink_rate(self.diam)
        self.base_size = self.diam / 2

        self.x = physics.update_movement(self.move_state, self.speed, self.x)
        physics.resize(self)
        physics.check_size_death(self.diam, self.life_state, self.move_state)

        physics.check_level_up(self,self.entitymanager)
        physics.check_death(self,self.game_state)

    def move(self, direction):
        if direction == 'LEFT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_LEFT)
        elif direction == 'RIGHT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_RIGHT)
        elif direction == 'NONE':
            self.move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)

    def draw(self):
        self.surface.fill((0, 0, 0, 0))

        pygame.draw.circle(self.surface, (255, 255, 255),
                           (self.base_size, self.base_size), self.base_size)

        self.rect.bottom = self.board_surface.get_height() - 100
        self.rect.centerx = int(self.x)
        self.board_surface.blit(self.surface, self.rect.topleft)

    def check_collisions(self,entities):
        for entity in entities:
            if self.rect.colliderect(entity.rect):
                if entity.type == EntityType.SNOWFLAKE:
                    physics.collect_snowflake(self,entity)
                    entity.collected()
                elif entity.type == EntityType.ROCK:
                    physics.handle_rock(self,entity)

    def reset(self):
        self.original_height = self.board_surface.get_height()
        self.diam = self.base_size
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)
        self.rect = self.surface.get_rect()
        self.speed = 5
        self.rect.bottom = self.y
        self.rect.centerx = int(self.x)
        self.current_level = 1
        self.level_up_size = physics.calculate_level_up_size(self.current_level)