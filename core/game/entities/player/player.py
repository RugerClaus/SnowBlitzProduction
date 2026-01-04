from core.game.entities.type import EntityType
from core.game.entities.entity import Entity
from core.state.GameLayer.Entities.Player.Intent.state import PLAYER_INTENT_STATE
from core.state.GameLayer.Entities.Player.Movement.statemanager import PlayerMoveStateManager
from core.state.GameLayer.Entities.Player.Powers.statemanager import PlayerPowerStateManager
from core.state.GameLayer.Entities.Player.Life.statemanager import PlayerLifeStateManager
from core.game.entities.player.playermechanics import PlayerMechanics as physics

class Player(Entity):
    def __init__(self, board_surface, entitymanager, sound, game_state):
        self.base_size = 10
        self.x = board_surface.get_width() // 2
        self.y = board_surface.get_height() - 100
        self.entitymanager = entitymanager
        self.game_state = game_state
        self.sound = sound
        super().__init__(self.x, self.y, board_surface, EntityType.PLAYER, self.base_size)
        self.reset()

        self.life_state = PlayerLifeStateManager()
        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()

        self.last_powerup_start_time = None
        self.powerup_duration = 5000
        self.shrink_rate = None

    def scale(self, event_h):
        scale_factor = event_h / self.original_height
        self.base_size = 10 * scale_factor
        self.diam = self.diam * scale_factor
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)

        self.board_surface.draw_circle(self.surface, (255, 255, 255), (self.base_size, self.base_size), float(self.base_size),self.type)

        self.y = event_h - self.base_size
        if self.y + self.base_size * 2 > self.board_surface.get_height():
            self.y = self.board_surface.get_height() - self.base_size * 2

        self.rect = self.surface.get_rect()
        self.rect.bottom = self.board_surface.get_height() - 100
        self.rect.centerx = self.board_surface.get_width() // 2 

    def center(self):
        self.x = self.board_surface.get_width() // 2

    def update(self):
        self.powerup_duration = physics.calculate_powerup_duration(self.score)
        self.shrink_rate = physics.calculate_shrink_rate(self.diam,self)
        self.diam -= self.shrink_rate
        self.base_size = self.diam / 2

        self.x = physics.update_movement(self.move_state, self.speed, self.x)
        physics.resize(self)
        physics.check_size_death(self.diam, self.life_state, self.move_state)

        physics.check_level_up(self,self.entitymanager)
        physics.check_power_state(self)
        physics.handle_powerup_timer(self)
        physics.handle_sfx(self)
        physics.check_death(self,self.game_state)
        physics.check_bounds(self)

    def move(self, direction):
        if direction == 'LEFT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_LEFT)
        elif direction == 'RIGHT':
            self.move_state.set_state(PLAYER_INTENT_STATE.MOVE_RIGHT)
        elif direction == 'NONE':
            self.move_state.set_state(PLAYER_INTENT_STATE.IDLE_MOVE)

    def draw(self):
        self.surface.fill((0, 0, 0, 0))

        self.board_surface.draw_circle(self.surface, self.color,
                           (self.base_size, self.base_size), self.base_size,self.type)

        self.rect.bottom = self.board_surface.get_height() - 100
        self.rect.centerx = int(self.x)
        self.board_surface.blit(self.surface, self.rect.topleft)
    
    def draw_wait(self):
        self.surface.fill(self.color)
        self.rect.bottom = self.board_surface.get_height() - 100
        self.rect.centerx = int(self.x)
        self.board_surface.blit(self.surface,self.rect.topleft)

    def check_collisions(self,entities):
        for entity in entities:
            if self.rect.colliderect(entity.rect):
                if entity.type == EntityType.SNOWFLAKE:
                    physics.collect_snowflake(self,entity)
                    self.sound.play_sfx('snow')
                    entity.collected()
                    self.score += entity.diam
                elif entity.type == EntityType.ROCK:
                    physics.handle_rock(self,entity)

                elif entity.type == EntityType.POWERUP:
                    physics.handle_powerup(self,entity)
                    entity.collected()
                    physics.apply_powerup(self,entity.power_type,self.powerup_duration)

                elif entity.type == EntityType.REDUCER:
                    physics.handle_reducer(self,entity)
                    entity.collected()

    def reset(self):
        self.original_height = self.board_surface.get_height()
        self.diam = 10
        self.surface = self.board_surface.make_surface(self.diam, self.diam, True)
        self.rect = self.surface.get_rect()
        self.speed = 5
        self.color = (255, 255, 255)
        self.rect.bottom = self.y
        self.rect.centerx = self.board_surface.get_width() // 2 
        self.x = self.rect.centerx

        self.score = 0
        self.current_level = 1
        self.level_up_size = physics.calculate_level_up_size(self.current_level)
        
        self.life_state = PlayerLifeStateManager()
        self.move_state = PlayerMoveStateManager()
        self.power_state = PlayerPowerStateManager()
        physics.reset_states(self)
        
        self.last_powerup_start_time = None
        self.powerup_duration = 5000
        self.shrink_rate = None

