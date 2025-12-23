import pygame
from core.game.modes.endless import Endless
from core.game.entities.player.player import Player
from core.game.controls import Controls
from core.game.entities.player.ui.sizebar import SizeBar, SizeBarManager

class SnowBlitz:
    def __init__(self,surface,sound,game_state):
        self.surface = surface
        self.player = Player(self.surface)
        self.sound = sound
        self.game_state = game_state
        self.controls = Controls()
        self.controls.set_controls(pygame.K_a,pygame.K_d)
        self.progress_bar = SizeBarManager(self.surface,self.player)

    def handle_event(self):
        
        keys = pygame.key.get_pressed()
        if keys[self.controls.move_left]:
            self.player.move('LEFT')
        elif keys[self.controls.move_right]:
            self.player.move('RIGHT')
        if not (keys[self.controls.move_left] or keys[self.controls.move_right]):
            self.player.move('NONE')

    def init_endless(self):
        game = Endless(self.surface,self.player,self.game_state)
        game.run()
        self.progress_bar.draw()
        
    def init_tutorial(self):
        game = Tutorial(self.surface)
        game.load_entity_buffers()
        game.load_environment()
        game.load_player()
        game.run()