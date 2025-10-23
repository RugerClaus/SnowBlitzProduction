import pygame

from core.state.state import GAMESTATE
from core.menus.pause import Pause
#from core.game.entities.entities import Entities
#from core.game.entities.EntityState.state import *
from core.game.camera.camera import Camera
from core.game.gamefuncs import GameSceneHandling
from core.game.SceneState.scene import MASTERSCENES
from core.game.SceneState.scenemanager import SceneManager
from core.game.entities.player import Player

class Game:
    def __init__(self,state,window,menu_callback,quit_callback):

        self.state = state
        self.window = window
        self.surface = window.make_surface(window.get_screen().get_width(),window.get_screen().get_height(),True)
        self.scene_handler = GameSceneHandling(self.surface)
        self.menu_callback = menu_callback
        self.quit_callback = quit_callback
        self.pause_menu = Pause(window,self.toggle_pause,self.quit_to_menu,self.quit,self.reset)
        #self.entity_manager = Entities()
        #self.entity_manager.players.append(Player())
        self.camera = Camera(self.window.get_screen().get_width,self.window.get_screen().get_height())
        self.scene = SceneManager()
        

    def main(self):
        if self.scene.is_scene(MASTERSCENES.INTROSCENE):
            self.scene_handler.introscene()
        elif self.scene.is_scene(MASTERSCENES.TUTORIALSCENE):
            self.scene_handler.tutorial_scene()
        elif self.scene.is_scene(MASTERSCENES.ROAMINGSCENE):
            self.scene_handler.roaming_scene()

    def toggle_pause(self):
        if not self.state.is_game_state(GAMESTATE.PAUSED):
            self.state.set_game_state(GAMESTATE.PAUSED)
        else:
            self.state.set_game_state(GAMESTATE.PLAYING)

    def handle_event(self,event,input):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            if event.key == pygame.K_SPACE:
                    self.toggle_color()
            if self.state.is_game_state(GAMESTATE.PAUSED):
                if event.key == pygame.K_9:
                    self.quit_to_menu()

        if self.state.is_game_state(GAMESTATE.PAUSED):
            self.pause_menu.handle_event(event)
        
        elif self.state.is_game_state(GAMESTATE.PLAYING):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.scene.set_scene(MASTERSCENES.INTROSCENE)
                elif event.key == pygame.K_2:
                    self.scene.set_scene(MASTERSCENES.TUTORIALSCENE)
                elif event.key == pygame.K_3:
                    self.scene.set_scene(MASTERSCENES.ROAMINGSCENE)
                
            input.handle_event(event,True)

            # for player in self.entity_manager.players:
            #     player.handle_event(event)

    def draw(self):
        self.window.blit(self.surface,(0,0))
        if self.state.is_game_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_game_state(GAMESTATE.PLAYING):
            pass
        

    def update(self):
        pass
        # for player in self.entity_manager.players:
        #     self.camera.update(player)

    def run(self):
        self.update()
        self.main()
        self.draw()
        

    def quit_to_menu(self):
        self.reset()
        pygame.event.clear()
        self.menu_callback()

    def quit(self):
        self.quit_callback()
    
    def reset(self):
        self.state.set_game_state(GAMESTATE.PLAYING)
        self.scene.set_scene(MASTERSCENES.INTROSCENE)
        print(str(self.scene.get_scene()))


# THE FOLLOWING ARE TESTING METHODS AND WILL BE COMMENTED OUT UNLESS USED:

    def toggle_color(self):
        print("pressed space")
        self.__test__toggle__color = not self.__test__toggle__color

