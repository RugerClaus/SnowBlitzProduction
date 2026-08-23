from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.state.ApplicationLayer.GameMode.state import GAME_MODE
from core.application.SnowBlitz.entities.type import EntityType
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

        self.system.input.CommandModule.sequences["go_to_next_season"] = [self.system.input.keys.zero_key()]
        self.system.input.CommandModule.sequences["reload_maps"] = [
                    self.system.input.keys.F1_key(),
                    self.system.input.keys.four_key()
                ]
        self.system.input.CommandModule.sequences["toggle_terrain_grid"] = [
                self.system.input.keys.F1_key(),
                self.system.input.keys.five_key()
            ]
        self.system.input.CommandModule.sequences["toggle_cloud_grid"] = [
                self.system.input.keys.F1_key(),
                self.system.input.keys.six_key()
            ]

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

    def handle_event(self,event,command=None):
        if event.type == self.system.input.keydown():
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

        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            if command == "go_to_next_season":
                self.game_object.environment.day_cycle.go_to_next_season()

            if command == "reload_maps":
                self.game_object.world.load_map_files()

            if command == "toggle_terrain_grid":
                self.game_object.world.toggle_map_grid("terrain0",red)
            if command == "toggle_cloud_grid":
                self.game_object.world.toggle_map_grid("cloud",purple)
        else:
            self.clear_debug_telemetry()

    def register_debug_telemetry(self):
        self.system.app_inspector["daytime"] = int(self.game_object.environment.day_cycle.current_time / 1000)
        self.system.app_inspector["brightness"] = self.game_object.environment.day_cycle.get_brightness()
        self.system.app_inspector["temperature"] = f"{self.game_object.environment.temperature.get_fahrenheit()} F,{self.game_object.environment.temperature.get_celsius()} C"
        self.system.app_inspector["Day"] = self.game_object.environment.day_cycle.day
        self.system.app_inspector["Season"] = self.game_object.environment.season.state.state
        self.system.app_inspector["Year"] = self.game_object.environment.day_cycle.year
        if self.game_object.player:
            self.system.app_inspector["shrinkrate"] = self.game_object.player.shrink_rate
            self.system.app_inspector["x_position"] = int(self.game_object.player.world_x * 10)
            
            snl = self.game_object.debug.draw_debug_snowflake_lines
            rkl = self.game_object.debug.draw_debug_rock_lines
            pul = self.game_object.debug.draw_debug_powerup_lines
            rel = self.game_object.debug.draw_debug_reducer_lines
            sl = self.game_object.debug.draw_debug_sun_line
            
            self.system.app_inspector["snowflk_tracers"] =  snl if snl is not False else None
            self.system.app_inspector["rock_tracers"] =  rkl if rkl is not False else None
            self.system.app_inspector["powerup_tracers"] =  pul if pul is not False else None
            self.system.app_inspector["reducer_tracers"] =  rel if rel is not False else None
            self.system.app_inspector["sun_tracer"] =  sl if sl is not False else None

    def clear_debug_telemetry(self):
        self.system.app_inspector["daytime"] = None
        self.system.app_inspector["brightness"] = None
        self.system.app_inspector["temperature"] = None
        self.system.app_inspector["Day"] = None
        self.system.app_inspector["Season"] = None
        self.system.app_inspector["Year"] = None
        self.system.app_inspector["shrinkrate"] = None
        self.system.app_inspector["snowflk_tracers"] = None
        self.system.app_inspector["rock_tracers"] = None
        self.system.app_inspector["powerup_tracers"] = None
        self.system.app_inspector["reducer_tracers"] = None
        self.system.app_inspector["sun_tracer"] = None

    def update(self):
        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.register_debug_telemetry()

    def draw(self):
        self._render_vector_lines()