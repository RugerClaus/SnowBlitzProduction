import pygame

class Controls:
    def __init__(self):
        self.move_left = pygame.K_a
        self.move_right = pygame.K_d

    def set_controls(self, move_left, move_right):
        self.move_left = move_left
        self.move_right = move_right