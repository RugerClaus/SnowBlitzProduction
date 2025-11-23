import pygame

from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager
from core.menus.pause import Pause
#from core.game.entities.entities import Entities
#from core.game.entities.EntityState.state import *

#this is for an imported game with a raycasting engine
#you'll see it's fairly easy to just drop pygame projects right in and tie them to everything else.
from core.game.entities.player.player import Player
from core.game.world.map import Map
from core.game.raycaster.raycaster import Raycaster
from core.game.raycaster.settings import WINDOW_WIDTH,WINDOW_HEIGHT
from helper import asset

class Game:
    def __init__(self,window,sound,menu_callback,quit_callback):

        self.state = GameStateManager()
        self.window = window
        self.surface = window.make_surface(WINDOW_WIDTH,WINDOW_HEIGHT,True)
        self.minimap_surface = window.make_surface(WINDOW_WIDTH//4,WINDOW_HEIGHT//4)
        self.sound = sound
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.pause_menu = Pause(window,self.toggle_pause,self.quit_to_menu,self.quit,self.reset)
        self.intent = None
        self.surface.fill('red')

        #below we handle the imported game
        self.player = Player(self.surface)
        self.map = Map(self.player)
        self.raycaster = Raycaster(self.player,self.map)


        self.backgroundimg = pygame.image.load(asset('background'))

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

        self.window.blit(self.surface,(self.window.get_width()//8,0))
        self.window.blit(self.minimap_surface,(0,self.surface.get_height() + 10))
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            self.surface.blit(self.backgroundimg,(0,0))

            self.map.update()

            self.player.update(self.map)

            self.raycaster.cast_all_rays()
            
            self.raycaster.draw_floor(self.surface)
            self.raycaster.draw(self.surface)
            self.map.draw(self.minimap_surface)
            self.player.draw(self.minimap_surface)
        

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

