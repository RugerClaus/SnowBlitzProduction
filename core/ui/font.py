import pygame
from helper import asset

class FontEngine:
    PRESETS = {
        "button": 60,
        "UI": 35,
        "dbug_state": 25,
        "game_over": 50,
        "keypress": 50,
        "default": 25
    }

    def __init__(self, type="default"):
        if isinstance(type, int):
            size = type
            self.font = pygame.font.Font(asset('default_font'), size)
        else:
            pygame.font.init()
            size = self.PRESETS.get(type, self.PRESETS["default"])
            self.font = pygame.font.Font(asset("default_font"), size)
