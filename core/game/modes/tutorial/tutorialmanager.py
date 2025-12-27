from core.state.GameLayer.GameMode.TutorialLayer.state import TUTORIALSTATE
from core.state.GameLayer.GameMode.TutorialLayer.statemanager import TutorialStateManager

class TutorialManager:
    def __init__(self, prompt, controls):
        self.state = TutorialStateManager()
        self.prompt = prompt
        self.controls = controls

    def start_tutorial_prompt(self):
        self.prompt.handle_start(self.controls)
        if self.prompt.player_has_moved:
            self.state.set_state(TUTORIALSTATE.BEGIN)
        else:
            self.prompt.display_movement_prompt()

    def start_tutorial(self,entitymanager):
        entitymanager.spawn_snowflakes()
        snowflakes = entitymanager.entities["snowflakes"]
        for snowflake in snowflakes:
            if snowflake.y >= entitymanager.board_surface.get_height() // 4:
                self.state.set_state(TUTORIALSTATE.SNOW_PROMPT)

    def prompt_player_start_snow(self):
        self.prompt.display_snow_instructions()
        self.prompt.player_has_continued = False
        self.prompt.handle_continue()
        if self.prompt.player_has_continued:
            self.state.set_state(TUTORIALSTATE.SNOW)