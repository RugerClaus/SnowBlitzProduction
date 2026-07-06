class Tutorial:
    def __init__(self, board_surface, player, entitymanager, controls, progress_bar,state,tutorial_manager, prompts):
        self.board_surface = board_surface
        self.player = player
        self.entitymanager = entitymanager
        self.controls = controls
        self.progress_bar = progress_bar
        self.prompts = prompts
        self.tutorial_state = state
        self.tutorial_manager = tutorial_manager

    def run(self):
        self.tutorial_manager.update()
        