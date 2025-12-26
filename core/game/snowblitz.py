import pygame
from core.game.modes.endless import Endless
from core.game.entities.player.player import Player
from core.game.controls import Controls
from core.game.entities.player.ui.sizebar import SizeBarManager
from core.game.entities.entitymanager import EntityManager
from core.game.entities.type import EntityType

class SnowBlitz:
    def __init__(self,board_surface,sound,game_state):
        self.board_surface = board_surface
        self.sound = sound
        self.game_state = game_state
        self.entitymanager = EntityManager(self.board_surface)
        self.player = Player(self.board_surface,self.entitymanager,game_state)
        self.controls = Controls()
        self.controls.set_controls(pygame.K_a,pygame.K_d)
        self.progress_bar = SizeBarManager(self.board_surface,self.player)
        

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls.move_left]:
            self.player.move('LEFT')
        elif keys[self.controls.move_right]:
            self.player.move('RIGHT')
        if not (keys[self.controls.move_left] or keys[self.controls.move_right]):
            self.player.move('NONE')

    def snowflakes(self):
        current_time = self.board_surface.get_current_time()

        if current_time - self.entitymanager.last_flake_spawn_time > 200:
            if len(self.entitymanager.entities["snowflakes"]) < 100:
                self.entitymanager.add_entity(EntityType.SNOWFLAKE)
                self.entitymanager.last_flake_spawn_time = current_time

    def rocks(self):
        current_time = self.board_surface.get_current_time()

        if current_time - self.entitymanager.last_rock_spawn_time > 200:
            if len(self.entitymanager.entities["rocks"]) < 20:
                self.entitymanager.add_entity(EntityType.ROCK)
                self.entitymanager.last_rock_spawn_time = current_time

    def init_endless(self):
        self.player.update()
        self.player.draw()
        self.progress_bar.update()
        self.progress_bar.draw()

        self.player.check_collisions(self.entitymanager.get_active_entities()) #will add self.sound here for passing sound effects to keep them the fuck out of the player class
        self.snowflakes()

        if self.player.current_level >= 3:
            self.rocks()
        # General entity handling
        self.entitymanager.update_entities()
        self.entitymanager.draw_entities()  
        
        
        
    def init_tutorial(self):
        pass

    def init_blitz(self):
        pass

    def resize(self, event_h):
        self.player.scale(event_h)
        self.progress_bar.update()
        self.progress_bar.draw()