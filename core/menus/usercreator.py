from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.network.user import User

class UserCreator:
    def __init__(self,main_menu):
        self.main_menu = main_menu
        self.user = User()

    def submit(self):
        
        self.main_menu.state.set_state(MENUSTATE.ROOT)
        self.main_menu.create_buttons()