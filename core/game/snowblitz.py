import pygame
from core.game.modes.endless import Endless
from core.game.modes.tutorial.tutorial import Tutorial
from core.game.modes.tutorial.prompts import Prompts
from core.game.entities.player.player import Player
from core.game.controls import Controls
from core.game.entities.player.ui.sizebar import SizeBarManager
from core.game.entities.entitymanager import EntityManager

class SnowBlitz:
    def __init__(self,board_surface,sound,game_state):
        self.board_surface = board_surface
        self.sound = sound
        self.game_state = game_state
        self.entitymanager = EntityManager(self.board_surface)
        self.player = Player(self.board_surface,self.entitymanager,sound,game_state)
        self.controls = Controls()
        self.controls.set_controls(pygame.K_a,pygame.K_d)
        self.start_time = self.board_surface.get_current_time()
        self.progress_bar = SizeBarManager(self.board_surface,self.player,self.start_time)
        

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls.move_left]:
            self.player.move('LEFT')
        elif keys[self.controls.move_right]:
            self.player.move('RIGHT')
        if not (keys[self.controls.move_left] or keys[self.controls.move_right]):
            self.player.move('NONE')

    def init_endless(self):
        endless = Endless(self.progress_bar,self.player,self.entitymanager)
        endless.run()
        
        
        
    def init_tutorial(self):
        prompts = Prompts(self.board_surface,self.player)
        tutorial = Tutorial(self.progress_bar,self.player,self.entitymanager,prompts,self.controls)
        tutorial.run()

    def init_blitz(self):
        pass

    def resize(self, event_h):
        self.player.scale(event_h)
        self.progress_bar.update()
        self.progress_bar.draw()

    def reset(self):
        self.player.reset()
        self.entitymanager.reset_entities()