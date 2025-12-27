import pygame
from core.ui.font import FontEngine

class Prompts():
    def __init__(self,board_surface,player):
        self.board_surface = board_surface
        self.surface = board_surface.make_surface(board_surface.get_width(), board_surface.get_height(), True)
        self.rect = self.surface.get_rect()
        self.player = player
        self.font = FontEngine(35).font
        self.player_has_moved = False
        self.player_has_continued = False
        self.prompt_text = None

    def display_movement_prompt(self):
        if not self.player_has_moved:
            self.prompt_text = "Press A or D to move"
            self.prompt = self.font.render(self.prompt_text,True,(255,255,128))
            self.prompt_rect = self.prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(self.prompt,self.prompt_rect)
        else:
            self.prompt_text = ""
            self.font.render(self.prompt_text,True,(255,255,128))
            self.board_surface.blit(self.prompt,self.prompt_rect)
            
    def display_snow_instructions(self):
        if not self.player_has_continued:
            prompt = self.font.render("Collide with snowflakes to grow \n \n Fill the size bar to level up \n \n \n PRESS SPACE TO CONTINUE",True,(255,255,128))
            prompt_rect = prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(prompt,prompt_rect)
    
    def display_rock_instructions(self):
        if not self.player_has_continued:
            prompt = self.font.render("Rocks are dangerous and can kill the player \n \n Move left and right to avoid them \n \n \n PRESS SPACE TO CONTINUE",True,(255,255,128))
            prompt_rect = prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(prompt,prompt_rect)

    def display_powerup_instructions(self):
        if not self.player_has_continued:
            prompt = self.font.render("Powerups are brightly colored \n \n Blue ones let you absorb the rock - Level Start: 5 \n \n Green ones stop you from shrinking - Level Start: 10 \n \n Red ones cause you to grow - Level Start: 20 \n \n \n PRESS SPACE TO CONTINUE",True,(255,255,128))
            prompt_rect = prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(prompt,prompt_rect)

    def display_level_reducer_instructions(self):
        if not self.player_has_continued:
            prompt = self.font.render("Level Reducers start at level 15 \n \n They lower the size threshold to level \n up based on the number on the item\n \n This will help in later levels so \n you don't grow bigger than the board_surface \n \n Press SPACE to continue",True,(255,255,128))
            prompt_rect = prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(prompt,prompt_rect)

    def display_end_board_surface(self):
        if not self.player_has_continued:
            prompt = self.font.render("Tutorial Complete! \n Good Job! \n \n Press SPACE to go to the main menu",True,(255,255,128))
            prompt_rect = prompt.get_rect(center=(self.board_surface.get_width()//2,self.board_surface.get_height()//2))
            self.board_surface.blit(prompt,prompt_rect)

    def handle_start(self,controls):
        keys = pygame.key.get_pressed()
        if keys[controls.move_left] or keys[controls.move_right]:
            self.player_has_moved = True
            
    def handle_continue(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player_has_continued = True