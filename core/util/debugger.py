import pygame

from core.ui.font import FontEngine
from core.state.ApplicationLayer.state import APPSTATE

class Debugger:
    def __init__(self,game,state,window):
        self.game = game
        self.state = state
        self.window = window
        self.surface = window.make_surface(window.get_screen().get_width(),window.get_screen().get_height(),True)
        self.rect = self.surface.get_rect()
        self.font = FontEngine("UI").font
        
    def create_options(self):
        pass

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if self.check_in_game_state():
                    print("In game")
                else:
                    print("Not in game")


    def draw(self):
        text_color = (255,255,255)
        self.surface.fill((0,0,0,0))
        surface_width = self.surface.get_width()
        fps = self.font.render(f"FPS: {round(self.window.get_fps())}",False,text_color)
        line_spacing = fps.get_height()

        appstate = self.font.render(f"Appstate: {str(self.state.app_state)}",False,text_color)



        self.surface.blit(fps,(0,0))
        self.surface.blit(appstate,(surface_width//2+surface_width//10,line_spacing*0.2))

        if self.state.is_app_state(APPSTATE.IN_GAME):
            game_state = self.font.render(f"{str(self.game.state.get_state())}",False,text_color)
            
            self.surface.blit(game_state,(surface_width//2+surface_width//10,line_spacing*1.2))

        self.window.blit(self.surface,self.rect)

    def update(self):
        pass