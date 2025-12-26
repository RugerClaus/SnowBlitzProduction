import pygame
from core.game.entities.snow.snowflake import SnowFlake
from core.game.entities.rock.rock import Rock
from core.game.entities.type import EntityType

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

    def reset_entities(self):
        self.entities = {
            "rocks": [],
            "powerups": [],
            "snowflakes": [],
            "level_reducers": []
        }

    def add_entity(self, entity_type):
        if entity_type == EntityType.ROCK:
            self.entities["rocks"].append(Rock(self.board_surface))
            
        elif entity_type == EntityType.SNOWFLAKE:
            self.entities["snowflakes"].append(SnowFlake(self.board_surface))

    def add_entities(self, entity_type, count):
        for _ in range(count):
            if entity_type == EntityType.ROCK:
                new_rock = Rock(self.board_surface)
                self.add_entity(new_rock)
            elif entity_type == EntityType.SNOWFLAKE:
                new_snowflake = SnowFlake(self.board_surface)
                self.add_entity(new_snowflake)

    def update_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.update()

    def draw_entities(self):
        for entity_list in self.entities.values():
            for entity in entity_list:
                entity.draw()

    def get_active_entities(self):
        active_entities = []
        for entity_list in self.entities.values():
            active_entities.extend(entity_list)
        return active_entities