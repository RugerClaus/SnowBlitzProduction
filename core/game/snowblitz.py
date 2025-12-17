import pygame
from core.game.modes.endless import Endless

class SnowBlitz:
    def __init__(self,surface,sound):
        self.surface = surface
        
    def init_endless(self):
        game = Endless(self.surface)
        game.load_entity_buffers()
        game.load_environment()
        game.load_player()
        game.run()