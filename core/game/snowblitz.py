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
    def __init__(self,system,game_state,mode):
        self.system = system
        self.game_state = game_state
        self.mode = mode

        self.endless = None
        self.tutorial = None
        self.blitz = None

        self.entitymanager = EntityManager(system)
        self.player = Player(system,self.entitymanager,game_state)
        self.start_time = self.system.window.get_current_time()
        self.progress_bar = PlayerUIManager(self.system.window,self.player)
        self.prompts = Prompts(self.system.window,self.player,self.system.input)
        self.tutorial_state = TutorialStateManager()

        # this stuff will take a while to iron out
        # self.day_cycle = DayCycle(self.system.window)
        # self.sun = Sun(self.system.window,self.day_cycle)

    def handle_event(self):

        keys = self.system.input.get_pressed_keys()

        if not keys[self.system.input.game_controls.slow]:
            if keys[self.system.input.game_controls.move_left]:
                self.player.move('LEFT')
            elif keys[self.system.input.game_controls.move_right]:
                self.player.move('RIGHT')
        else:
            if keys[self.system.input.game_controls.move_left]:
                self.player.move('SLOW_LEFT')
            elif keys[self.system.input.game_controls.move_right]:
                self.player.move('SLOW_RIGHT')
        if not (keys[self.system.input.game_controls.move_left] or keys[self.system.input.game_controls.move_right]):
            self.player.move('NONE')

        #below is setup for spawning in entities and other game functions that need to be tested.
        #i could be less messy about it since I do have a centralized system for input, but this will keep it nice and scoped
        

    def draw(self):
        if self.mode.is_state(GAME_MODE.ENDLESS):
            if self.endless is None:
                self.endless = Endless(self.progress_bar, self.player, self.entitymanager)
            self.endless.run()
        elif self.mode.is_state(GAME_MODE.TUTORIAL):
            if self.tutorial is None:
                tutorial_manager = TutorialManager(self.system.window, self.prompts,self.system.input.game_controls,self.entitymanager,self.player,self.progress_bar,self.tutorial_state)
                self.tutorial = Tutorial(self.system.window,self.player,self.entitymanager,self.system.input.game_controls,self.progress_bar,self.tutorial_state,tutorial_manager,self.prompts)
            self.tutorial.run()
        elif self.mode.is_state(GAME_MODE.BLITZ):
            if self.blitz is None:
                self.blitz = Blitz(self.progress_bar, self.player, self.entitymanager)
            self.blitz.run()

    def resize(self, event_h):
        self.player.scale(event_h)
        self.player.center()
        self.progress_bar.update()
        self.progress_bar.draw()

    def reset(self):
        self.tutorial_state.set_state(TUTORIALSTATE.RESET)
        self.player.reset()
        self.progress_bar.reset_timer()
        self.progress_bar.draw()
        self.entitymanager.reset_entities()
        self.entitymanager.reset_spawn_timers()