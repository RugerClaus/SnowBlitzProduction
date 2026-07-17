from core.state.ApplicationLayer.GameMode.state import GAME_MODE
from core.application.entities.type import EntityType
from core.util.colors import *

class SBDebugUtils:
    def __init__(self,system,game_object):
        self.system = system
        self.game_object = game_object

        self.draw_debug_snowflake_lines = False
        self.draw_debug_rock_lines = False
        self.draw_debug_powerup_lines = False
        self.draw_debug_reducer_lines = False
        self.draw_debug_sun_line = False

    def toggle_debug_snowflake_lines(self):
        self.draw_debug_snowflake_lines = not self.draw_debug_snowflake_lines

    def toggle_debug_rock_lines(self):
        self.draw_debug_rock_lines = not self.draw_debug_rock_lines

    def toggle_debug_powerup_lines(self):
        self.draw_debug_powerup_lines = not self.draw_debug_powerup_lines

    def toggle_debug_reducer_lines(self):
        self.draw_debug_reducer_lines = not self.draw_debug_reducer_lines

    def toggle_debug_sun_line(self):
        self.draw_debug_sun_line = not self.draw_debug_sun_line

    def _render_vector_lines(self):
        if not self.game_object.mode.is_state(GAME_MODE.NONE):
            for entity in self.game_object.entitymanager.get_active_entities():
                if self.draw_debug_snowflake_lines:
                    if entity.type == EntityType.SNOWFLAKE:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,red,width=2)
                if self.draw_debug_rock_lines:    
                    if entity.type == EntityType.ROCK:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,green,width=2)
                if self.draw_debug_powerup_lines:    
                    if entity.type == EntityType.POWERUP:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,white,width=2)
                if self.draw_debug_reducer_lines:
                    if entity.type == EntityType.REDUCER:
                        self.system.window.draw_line(self.system.window.get_screen(),entity.rect.center,self.game_object.player.rect.center,blue,width=2)
            if self.draw_debug_sun_line:
                if self.game_object.environment.sun.x > 0:
                    self.system.window.draw_line(self.system.window.get_screen(),self.game_object.environment.sun.rect.center,self.game_object.player.rect.center,purple,width=2)

    def handle_event(self,event):
        if event.key == self.system.input.keys.seven_key():
            self.game_object.player.current_level = 19

        elif event.key == self.system.input.keys.h_key():
            self.game_object.player.current_level = 15

        elif event.key == self.system.input.keys.F3_key():
            self.game_object.debug.toggle_debug_snowflake_lines()

        elif event.key == self.system.input.keys.F4_key():
            self.game_object.debug.toggle_debug_rock_lines()

        elif event.key == self.system.input.keys.F5_key():
            self.game_object.debug.toggle_debug_powerup_lines()

        elif event.key == self.system.input.keys.F6_key():
            self.game_object.debug.toggle_debug_reducer_lines()
            
        elif event.key == self.system.input.keys.F7_key():
            self.game_object.debug.toggle_debug_sun_line()

    def draw(self):
        self._render_vector_lines()