import pygame,random
from core.state.GameLayer.state import GAMESTATE
from core.game.entities.entitymanager import EntityManager
from core.game.entities.type import EntityType

class Endless:
    def __init__(self,surface,player,game_state):
        self.surface = surface
        self.player = player
        self.game_state = game_state
        self.entitymanager = EntityManager(self.surface)

    def run(self):
        if not self.player.is_alive():
            self.game_state.set_state(GAMESTATE.GAME_OVER)
            return
        self.player.update()
        self.player.draw()
        
        current_time = pygame.time.get_ticks()

        # Spawn snowflakes with time-based logic
        self.entitymanager.add_entity(EntityType.SNOWFLAKE)
        if current_time - self.entitymanager.last_flake_spawn_time > 2000:
            if len(self.entities["snowflakes"]) < 100:
                self.entitymanager.add_entity(EntityType.SNOWFLAKE)
                self.entitymanager.last_flake_spawn_time = current_time
                self.flake_spawn_interval = random.randint(100, 200)

        # General entity handling
        
        self.entitymanager.draw_snowflakes()  