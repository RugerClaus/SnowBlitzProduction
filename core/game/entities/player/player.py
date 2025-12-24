import pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.GameLayer.Entities.Player.Powers.statemanager import PlayerPowerStateManager
from core.state.GameLayer.Entities.Player.Life.state import PLAYER_LIFE_STATE
from core.state.GameLayer.Entities.Player.Life.statemanager import PlayerLifeStateManager
from core.state.GameLayer.Entities.Player.Status.state import PLAYER_STATUS_STATE
from core.state.GameLayer.Entities.Player.Status.statemanager import PlayerStatusStateManager
from core.game.entities.player.playermechanics import PlayerMechanics as pm

class Player(Entity):
    def __init__(self, board_surface):
        self.board_surface = board_surface
        self.original_height = board_surface.get_height()
        self.base_size = 10  # Base size of player at original screen height
        self.x = board_surface.get_width() // 2
        self.y = board_surface.get_height() - 100
        super().__init__(self.x, self.y, EntityType.PLAYER, self.base_size)
        self.diam = self.base_size * 2
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)
        self.rect = self.surface.get_rect()
        self.speed = 3
        self.rect.center = (int(self.x), int(self.y))
        self.level_up_size = 20

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

        self.y = event_h - 100  # Keep player at a fixed position relative to screen height
        self.rect = self.surface.get_rect()
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.diam -= pm.calculate_shrink_rate(self.diam)
        self.base_size = self.diam / 2

        self.x = pm.update_movement(self.move_state, self.speed, self.x)
        
        pm.check_death(self.diam, self.life_state, self.move_state)

        self.rect.centery = self.y

    def move(self, direction):
        if direction == 'LEFT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_LEFT)
        elif direction == 'RIGHT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_RIGHT)
        elif direction == 'NONE':
            self.move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)

    def draw(self):
        self.board_surface.fill((0, 0, 0, 0))
        self.surface.fill((0, 0, 0, 0))

        pygame.draw.circle(self.surface, (255, 255, 255),
                           (self.base_size, self.base_size), self.base_size)

        self.rect.center = (int(self.x), int(self.y))
        self.board_surface.blit(self.surface, self.rect.topleft)
