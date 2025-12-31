import pygame
from core.game.modes.endless import Endless
from core.game.modes.tutorial.tutorial import Tutorial
from core.game.entities.player.player import Player
from core.game.controls import Controls
from core.game.entities.player.ui.sizebar import SizeBarManager, SizeBar
from core.game.entities.entitymanager import EntityManager

from core.game.modes.tutorial.tutorialmanager import TutorialManager
from core.game.modes.tutorial.prompts import Prompts
from core.state.GameLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE

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
        
        self.prompts = Prompts(self.board_surface,self.player)
        self.tutorial_state = TutorialStateManager()
        self.tutorial_manager = TutorialManager(self.board_surface, self.prompts,self.controls,self.entitymanager,self.player,self.progress_bar,self.tutorial_state)

        self.tutorial = Tutorial(self.board_surface,self.player,self.entitymanager,self.controls,self.progress_bar,self.tutorial_state,self.tutorial_manager,self.prompts)
        
        

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
        self.tutorial.run()

    def init_blitz(self):
        pass

    def resize(self, event_h):
        self.player.scale(event_h)
        self.progress_bar.update()
        self.progress_bar.draw()

    def reset(self):
        self.player.reset()
        self.entitymanager.reset_entities()
    
    def reset_tutorial(self):
        self.reset()
        self.tutorial_state.set_state(TUTORIALSTATE.RESET)