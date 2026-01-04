import pygame

from core.ui.font import FontEngine
from core.state.ApplicationLayer.state import APPSTATE

class Debugger:
    def __init__(self,game,state,window,sound,loading):
        self.sound = sound
        self.game = game
        self.state = state
        self.window = window
        self.loading = loading
        self.surface = window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()
        self.font_left = FontEngine("UI").font
        self.font_right = FontEngine("dbug_state").font
        
    def create_options(self):
        pass

    def scale(self):
        self.surface = self.window.draw_overlay((0, 0, 0), 128)
        self.rect = self.surface.get_rect()

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if self.check_in_game_state():
                    print("In game")
                else:
                    print("Not in game")
        if event.type == pygame.VIDEORESIZE:
            self.scale()
    

    def draw(self):
        text_color = (255, 255, 255)
        self.surface.fill((0, 0, 0, 0.5))
        surface_width = self.surface.get_width()
        
        # Left side
        left_x = 10
        left_y = 10
        line_spacing = 20  # fallback spacing

        # FPS
        fps_text = f"FPS: {round(self.window.get_fps())}"
        fps_surf = self.font_left.render(fps_text, False, text_color)
        self.surface.blit(fps_surf, (left_x, left_y))
        left_y += fps_surf.get_height() * 1.2

        # Current song
        stripped_title = self.sound.current_track.rsplit('.', 1)[0] if self.sound.current_track else None
        song_text = f"Song: {stripped_title or 'None'}"
        
        song_surf = self.font_left.render(song_text, False, text_color)
        self.surface.blit(song_surf, (left_x, left_y))
        left_y += song_surf.get_height() * 1.2

        # Right side hierarchical state
        right_x = surface_width - 10
        right_y = 10

        # App state
        appstate_text = f"APPSTATE: {self.state.get_state()}"
        appstate_surf = self.font_right.render(appstate_text, False, text_color)
        self.surface.blit(appstate_surf, (right_x - appstate_surf.get_width(), right_y))
        right_y += appstate_surf.get_height() * 1.2

        if self.state.is_state(APPSTATE.LOADING):
            load_state_text = f"{self.loading.state.get_state()}"
            load_state_surf = self.font_right.render(load_state_text,False,text_color)
            self.surface.blit(load_state_surf,(right_x - load_state_surf.get_width(),right_y))
            right_y += load_state_surf.get_height() * 1.2

        # Game state (if in game)
        if self.state.is_state(APPSTATE.IN_GAME):
            #master game state
            game_state_text = f"{self.game.state.get_state()}"
            game_state_surf = self.font_right.render(game_state_text, False, text_color)
            self.surface.blit(game_state_surf, (right_x - game_state_surf.get_width(), right_y))
            right_y += game_state_surf.get_height() * 1.2

            #game mode
            game_mode_text = f"{self.game.game_mode.get_state()}"
            game_mode_surf = self.font_right.render(game_mode_text, False, text_color)
            self.surface.blit(game_mode_surf,(right_x - game_state_surf.get_width(), right_y))
            right_y += game_mode_surf.get_height() * 1.2

            #player life state
            player_life_state_text = f"Player Life: {self.game.game_object.player.life_state.get_state()}"
            player_life_state_surf = self.font_right.render(player_life_state_text, False, text_color)
            self.surface.blit(player_life_state_surf, (right_x - player_life_state_surf.get_width(), right_y))
            right_y += player_life_state_surf.get_height() * 1.2

            #player_movement_state
            player_movement_state_text = f"Player Movement: {self.game.game_object.player.move_state.get_state()}"
            player_movement_state_surf = self.font_right.render(player_movement_state_text, False, text_color)
            self.surface.blit(player_movement_state_surf, (right_x - player_movement_state_surf.get_width(), right_y))
            right_y += player_movement_state_surf.get_height() * 1.2

            #player_movement_state
            player_power_state_text = f"Player Movement: {self.game.game_object.player.power_state.get_state()}"
            player_power_state_surf = self.font_right.render(player_power_state_text, False, text_color)
            self.surface.blit(player_power_state_surf, (right_x - player_power_state_surf.get_width(), right_y))
            right_y += player_power_state_surf.get_height() * 1.2

        # Finally, blit the surface
        self.window.blit(self.surface, self.rect)


    def update(self):
        pass