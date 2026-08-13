from core.application.network.leaderboard import Leaderboard
class Gen_Utility:
    def __init__(self,dr):
        self.dr = dr
        self.app = dr.application
        self.system = dr.system
        
        self.lb = Leaderboard(dr.system)
        
        self.system.input.CommandModule.sequences["get data in leaderboard package"] = [dr.system.input.keys.x_key(),dr.system.input.keys.nine_key()]

    def handle_event(self,event,command=None):

        if command == "get data in leaderboard package":
            self.lb.get_logged_in_user_score()