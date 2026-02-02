import pygame

class Keys:
    def __init__(self):
        self.info = "This is a class of methods to return pygame keys, but can work for any other backend."
        #will make the whole system more robust so i can clean out and modularize the input system.

    def space_key(self):
        return pygame.K_SPACE
    
    def a_key(self):
        return pygame.K_a
    
    def d_key(self):
        return pygame.K_d