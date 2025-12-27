import pygame,random
from core.game.entities.snow.snowflake import SnowFlake
from core.game.entities.rock.rock import Rock

from core.game.entities.powerups.absorb_rock import AbsorbRock
from core.game.entities.powerups.anti_shrink import AntiShrink

from core.game.entities.reducers.twenty import Twenty
from core.game.entities.reducers.fifty import Fifty
from core.game.entities.reducers.hundred import OneHundred

from core.game.entities.type import EntityType
from core.game.entities.powerups.type  import PowerUpType
from core.game.entities.reducers.type import LRType

class EntityManager:
    def __init__(self, board_surface):
        self.board_surface = board_surface
        self.entities = {
            "rocks": [],
            "powerups": [],
            "snowflakes": [],
            "level_reducers": []
        }

        self.last_flake_spawn_time = pygame.time.get_ticks()
        self.last_rock_spawn_time = pygame.time.get_ticks()
        self.last_powerup_spawn_time = pygame.time.get_ticks()
        self.last_reducer_spawn_time = pygame.time.get_ticks()

        self.flake_interval = 500
        self.rock_interval = 800
        self.powerup_interval = 1500
        

    def reset_entities(self):
        self.entities = {
            "rocks": [],
            "powerups": [],
            "snowflakes": [],
            "level_reducers": []
        }

    def add_entity(self, entity_type, sub_type=None):
        if sub_type is None:
            if entity_type == EntityType.ROCK:
                self.entities["rocks"].append(Rock(self.board_surface))
                
            elif entity_type == EntityType.SNOWFLAKE:
                self.entities["snowflakes"].append(SnowFlake(self.board_surface))

        else:
            if isinstance(sub_type,PowerUpType):
                if sub_type == PowerUpType.ABSORB_ROCK:
                    self.entities["powerups"].append(AbsorbRock(self.board_surface))
                elif sub_type == PowerUpType.ANTI_SHRINK:
                    self.entities["powerups"].append(AntiShrink(self.board_surface))
            elif isinstance(sub_type,LRType):
                if sub_type == LRType.TWENTY:
                    self.entities["level_reducers"].append(Twenty(self.board_surface))
                elif sub_type == LRType.FIFTY:
                    self.entities["level_reducers"].append(Fifty(self.board_surface))
                elif sub_type == LRType.ONE_HUNDRED:
                    self.entities["level_reducers"].append(OneHundred(self.board_surface))

    def update_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.update()
        self.reducer_interval = random.randint(5000,10000)

    def draw_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.draw()

    def get_active_entities(self):
        active_entities = []
        for entity_list in self.entities.values():
            active_entities.extend(entity_list)
        return active_entities
    
    def check_collisions(self):
        rocks = self.entities["rocks"]
        snowflakes = self.entities["snowflakes"]

        for rock in rocks:
            for snowflake in snowflakes:

                if rock.rect.colliderect(snowflake.rect):
                    snowflake.rect.top += rock.rect.bottom + 5
                    snowflake.speed = rock.speed + 1

    def spawn_snowflakes(self):
        current_time = self.board_surface.get_current_time()
        if current_time - self.last_flake_spawn_time > self.flake_interval:
            if len(self.entities["snowflakes"]) < 100:
                self.add_entity(EntityType.SNOWFLAKE)
                self.last_flake_spawn_time = current_time

    def spawn_rocks(self,current_level):
        current_time = self.board_surface.get_current_time()

        if current_time - self.last_rock_spawn_time > self.rock_interval:
            if len(self.entities["rocks"]) < 5:
                if current_level >= 3:
                    self.add_entity(EntityType.ROCK)
                    self.last_rock_spawn_time = current_time
    
    def spawn_powerups(self,current_level):
        current_time = self.board_surface.get_current_time()

        if current_time - self.last_powerup_spawn_time > self.powerup_interval:
            if len(self.entities["powerups"]) < 5:
                if current_level >= 5:
                    self.add_entity(EntityType.POWERUP,PowerUpType.ABSORB_ROCK)
                    self.last_powerup_spawn_time = current_time
                if current_level >= 10:
                    self.add_entity(EntityType.POWERUP,PowerUpType.ANTI_SHRINK)
                    self.last_powerup_spawn_time = current_time

    def spawn_reducers(self,current_level):
        current_time = self.board_surface.get_current_time()

        if current_time - self.last_reducer_spawn_time > self.reducer_interval:
            
            if len(self.entities["level_reducers"]) < 2:
                if current_level >= 15 and current_level < 30:
                    self.add_entity(EntityType.REDUCER,LRType.TWENTY)
                    self.last_reducer_spawn_time = current_time
                elif current_level >= 30 and current_level < 50:
                    reducer_choice = random.choice([LRType.TWENTY,LRType.FIFTY])
                    self.add_entity(EntityType.REDUCER,reducer_choice)
                    self.last_reducer_spawn_time = current_time
                elif current_level >= 50:
                    reducer_choice = random.choice([LRType.TWENTY,LRType.FIFTY,LRType.ONE_HUNDRED])
                    self.add_entity(EntityType.REDUCER,reducer_choice)
                    self.last_reducer_spawn_time = current_time