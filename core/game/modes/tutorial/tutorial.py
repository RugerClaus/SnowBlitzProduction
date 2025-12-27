from core.game.modes.tutorial.tutorialmanager import TutorialManager
from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE

class Tutorial:
    def __init__(self, progress_bar, player, entitymanager, prompts, controls):
        self.progress_bar = progress_bar
        self.player = player
        self.entitymanager = entitymanager
        self.prompts = prompts
        self.controls = controls

    def run(self):
        
        pass