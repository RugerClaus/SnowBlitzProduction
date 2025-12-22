import pygame
from core.game.modes.endless import Endless
from core.game.entities.player.player import Player

class SnowBlitz:
    def __init__(self,surface,sound):
        self.surface = surface
        self.player = Player(self.surface)
        self.sound = sound

    def init_endless(self):
        game = Endless(self.surface,self.player)
        game.run()