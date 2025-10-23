import pygame
from helper import asset

class FontEngine():
    def __init__(self,type):
        pygame.font.init()
        self.type = type
        self.font = None
        if self.type == "button":
            self.button_font()
        elif self.type == "UI":
            self.ui_font()
        elif self.type == "GameOver":
            self.game_over_font()
        elif self.type == "keypress":
            self.key_press_font()
        else:
            self.default_font()

    def button_font(self):
        self.font = pygame.font.Font(asset("default_font"), 60)
        
    def ui_font(self):
        self.font = pygame.font.SysFont('Arial', 40)
    def game_over_font(self):
        self.font = pygame.font.Font(asset("default_font"), 120)
    def key_press_font(self):
        self.font = pygame.font.Font(asset("default_font"), 200)
    def default_font(self):
        self.font = pygame.font.Font(asset("default_font"), 25)