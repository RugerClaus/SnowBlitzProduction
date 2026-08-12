class SnowBlitz:
    def __init__(self,application):
        self.application = application
        self.system = self.application.system

    def init_player(self):
        if self.player is None:
            self.player = Player(self.system,self.entitymanager,self.application.game_state,self.environment,self.session)
        if self.hud is None:
            self.hud = PlayerUIManager(self.system,self.player)
