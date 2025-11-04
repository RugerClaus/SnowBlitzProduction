import pygame

from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.menus.pause import Pause
#from core.game.entities.entities import Entities
#from core.game.entities.EntityState.state import *
from core.game.world.world import World
from core.game.camera.camera import Camera
from core.game.entities.player import Player

class Game:
    def __init__(self,window,sound,menu_callback,quit_callback):

        self.state = GameStateManager()
        self.window = window
        self.surface = window.make_surface(window.get_screen().get_width(),window.get_screen().get_height(),True)
        self.sound = sound
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.pause_menu = Pause(window,self.toggle_pause,self.quit_to_menu,self.quit,self.reset)
        self.world = World(window)
        self.camera = Camera(self.surface.get_width,self.surface.get_height())
        self.intent = None
        self.surface.fill('red')

    def toggle_pause(self):
        if not self.state.is_state(GAMESTATE.PAUSED):
            self.state.set_state(GAMESTATE.PAUSED)
        else:
            self.state.set_state(GAMESTATE.PLAYING)

    def handle_event(self,event,input):
        input.handle_event(event,True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
        
        if self.state.is_state(GAMESTATE.PLAYING):
            if event.type == pygame.KEYDOWN:
                pass
                

        elif self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if input.last_key == pygame.K_9:
                    self.quit_to_menu()
        

    def draw(self):
        self.window.blit(self.surface,(0,0))
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.world.create()
        

    def update(self):
        pass

    def run(self):

        self.update()
        self.draw()
        

    def quit_to_menu(self):
        self.reset()
        pygame.event.clear()
        self.menu_callback()

    def quit(self):
        self.quit_callback()
    
    def reset(self):
        self.state.set_state(GAMESTATE.PLAYING)

