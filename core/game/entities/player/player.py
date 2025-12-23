import pygame
from core.game.entities.type import EntityType
from core.game.entities.entity import Entity
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Powers.state import PLAYER_POWER_STATE
from core.state.GameLayer.Entities.Player.Powers.statemanager import PlayerPowerStateManager

class Player(Entity):
    def __init__(self, board_surface):
        self.base_size = 10  # radius in logical pixels
        self.board_surface = board_surface
        x = board_surface.get_width() // 2
        y = board_surface.get_height() - 100  # Initial y value is 100px above bottom
        super().__init__(x, y, EntityType.PLAYER, self.base_size)
        self.diam = self.base_size * 2
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)
        self.rect = self.surface.get_rect()

        self.speed = 3
        self.rect.center = (int(self.x), int(self.y))

        self.level_up_size = 20

        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()

    def scale(self, event_w, event_h):
        # Adjust base size relative to the new height to scale player size
        scale_factor = event_h / self.board_surface.get_height()
        self.base_size = 10 * scale_factor  # Adjust base size (player size)
        self.diam = self.base_size * 2

        # Resize the player's surface accordingly
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)
        
        # Draw the resized player (circle) onto the resized surface
        pygame.draw.circle(self.surface, (255, 255, 255), 
                           (self.base_size, self.base_size), self.base_size)

        # Adjust the player's y position to remain 100px from the bottom
        self.y = event_h - 100  # Keep 100px above bottom
        self.rect = self.surface.get_rect()
        self.rect.center = (int(self.x), int(self.y))  # Update position on the new surface

    def update(self):
        # Update player's movement
        if self.move_state.is_state(PLAYER_INTENT_STATE.MOVE_LEFT):
            self.x -= self.speed
        elif self.move_state.is_state(PLAYER_INTENT_STATE.MOVE_RIGHT):
            self.x += self.speed
        elif self.move_state.is_state(PLAYER_INTENT_STATE.IDLE_MOVE):
            self.speed += 0

        if not self.move_state.is_state(PLAYER_INTENT_STATE.IDLE_MOVE):
            print(f"Player position: x={self.x}, y={self.y}")

        # Update the player's rect.center position after movement
        self.rect.center = (int(self.x), int(self.y))

    def move(self, direction):
        if direction == 'LEFT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_LEFT)
        elif direction == 'RIGHT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_RIGHT)
        elif direction == 'NONE':
            self.move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)

    def draw(self):
        # Clear previous surface and redraw the player on the board surface
        self.board_surface.fill((0, 0, 0, 0))  # Clear previous surface
        self.surface.fill((0, 0, 0, 0))  # Clear the player's surface
        
        # Redraw the player (now it should be properly scaled and positioned)
        pygame.draw.circle(self.surface, (255, 255, 255),
                           (self.base_size, self.base_size), self.base_size)

        # Update the rect center after any changes
        self.rect.center = (int(self.x), int(self.y))
        self.board_surface.blit(self.surface, self.rect.topleft)
