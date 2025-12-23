import pygame
from core.game.modes.endless import Endless
from core.game.entities.player.player import Player
from core.game.controls import Controls
from core.game.entities.player.ui.sizebar import SizeBar, SizeBarManager

class SnowBlitz:
    def __init__(self,surface,sound):
        self.surface = surface
        self.player = Player(self.surface)
        self.sound = sound
        self.controls = Controls()
        self.controls.set_controls(pygame.K_a,pygame.K_d)
        self.progress_bar = SizeBarManager(self.surface,self.player)

    def handle_event(self,event):
        
        keys = pygame.key.get_pressed()
        if keys[self.controls.move_left]:
            self.player.move('LEFT')
        elif keys[self.controls.move_right]:
            self.player.move('RIGHT')
        if not (keys[self.controls.move_left] or keys[self.controls.move_right]):
            self.player.move('NONE')

    def init_endless(self):
        game = Endless(self.surface,self.player)
        self.progress_bar.update()
        self.progress_bar.draw()
        game.run()

        
    def init_tutorial(self):
        game = Tutorial(self.surface)
        game.load_entity_buffers()
        game.load_environment()
        game.load_player()
        game.run()