from core.state.GameLayer.GameMode.state import GAME_MODE
from core.application.entities.type import EntityType

class SBDebugUtils:
    def __init__(self,system,game_object):
        self.system = system
        self.game_object = game_object

        self.draw_debug_snowflake_lines = False
        self.draw_debug_rock_lines = False
        self.draw_debug_powerup_lines = False
        self.draw_debug_reducer_lines = False

    def toggle_debug_snowflake_lines(self):
        self.draw_debug_snowflake_lines = not self.draw_debug_snowflake_lines

    def toggle_debug_rock_lines(self):
        self.draw_debug_rock_lines = not self.draw_debug_rock_lines

    def toggle_debug_powerup_lines(self):
        self.draw_debug_powerup_lines = not self.draw_debug_powerup_lines

    def toggle_debug_reducer_lines(self):
        self.draw_debug_reducer_lines = not self.draw_debug_reducer_lines

    def draw_vector_lines(self):
        if not self.game_object.mode.is_state(GAME_MODE.NONE):
            for entity in self.game_object.entitymanager.get_active_entities():
                if self.draw_debug_snowflake_lines:
                    if entity.type == EntityType.SNOWFLAKE:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,(255,0,0))
                if self.draw_debug_rock_lines:    
                    if entity.type == EntityType.ROCK:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,(0,255,0))
                if self.draw_debug_powerup_lines:    
                    if entity.type == EntityType.POWERUP:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,(255,255,255))
                if self.draw_debug_reducer_lines:
                    if entity.type == EntityType.REDUCER:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,(0,0,255))

    def draw(self):
        self.draw_vector_lines()