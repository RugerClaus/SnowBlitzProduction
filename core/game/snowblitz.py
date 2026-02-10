import math
from core.game.modes.endless import Endless
from core.game.modes.blitz import Blitz
from core.game.modes.tutorial.tutorial import Tutorial
from core.game.entities.player.player import Player
from core.game.entities.player.ui.uimanager import PlayerUIManager
from core.game.entities.entitymanager import EntityManager
from core.game.modes.tutorial.tutorialmanager import TutorialManager
from core.game.modes.tutorial.prompts import Prompts
from core.state.GameLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE

from core.game.entities.type import EntityType
from core.game.entities.powerups.type import PowerUpType

from core.state.GameLayer.GameMode.state import GAME_MODE

# from core.game.mechanics.daycycle.daycycle import DayCycle
# from core.game.entities.sun.sun import Sun

class SnowBlitz:
    def __init__(self,board_surface,sound,game_state,input,mode):
        self.board_surface = board_surface
        self.sound = sound
        self.game_state = game_state
        self.input = input
        self.mode = mode
        self.entitymanager = EntityManager(self.board_surface)
        self.player = Player(self.board_surface,self.entitymanager,sound,game_state)
        self.start_time = self.board_surface.get_current_time()
        self.progress_bar = PlayerUIManager(self.board_surface,self.player)
        self.prompts = Prompts(self.board_surface,self.player,self.input)
        self.tutorial_state = TutorialStateManager()
        self.tutorial_manager = TutorialManager(self.board_surface, self.prompts,self.input.game_controls,self.entitymanager,self.player,self.progress_bar,self.tutorial_state)
        self.tutorial = Tutorial(self.board_surface,self.player,self.entitymanager,self.input.game_controls,self.progress_bar,self.tutorial_state,self.tutorial_manager,self.prompts)

        # this stuff will take a while to iron out
        # self.day_cycle = DayCycle(self.board_surface)
        # self.sun = Sun(self.board_surface,self.day_cycle)

    def handle_event(self):
        keys = self.input.get_pressed_keys()

        if not keys[self.input.game_controls.slow]:
            if keys[self.input.game_controls.move_left]:
                self.player.move('LEFT')
            elif keys[self.input.game_controls.move_right]:
                self.player.move('RIGHT')
        else:
            if keys[self.input.game_controls.move_left]:
                self.player.move('SLOW_LEFT')
            elif keys[self.input.game_controls.move_right]:
                self.player.move('SLOW_RIGHT')
        if not (keys[self.input.game_controls.move_left] or keys[self.input.game_controls.move_right]):
            self.player.move('NONE')

        #below is setup for spawning in entities and other game functions that need to be tested.
        #i could be less messy about it since I do have a centralized system for input, but this will keep it nice and scoped

        if keys[self.input.keys.h_key()]:
            self.entitymanager.add_entity(EntityType.POWERUP,PowerUpType.SPEED_BOOST)
        
    def init_endless(self):
        endless = Endless(self.progress_bar, self.player, self.entitymanager)
        endless.run()
        
    def init_tutorial(self):
        self.board_surface.fill((0,0,0))
        self.tutorial.run()

    def init_blitz(self):
        blitz = Blitz(self.progress_bar,self.player,self.entitymanager)
        blitz.run()

    def resize(self, event_h):
        self.player.scale(event_h)
        self.player.center()
        self.progress_bar.update()
        self.progress_bar.draw()

    def reset(self):
        self.player.reset()
        self.progress_bar.reset_timer()
        self.progress_bar.draw()
        self.entitymanager.reset_entities()
    
    def reset_tutorial(self):
        self.reset()
        self.tutorial_state.set_state(TUTORIALSTATE.RESET)