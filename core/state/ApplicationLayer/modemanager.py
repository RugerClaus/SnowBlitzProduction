from core.state.ApplicationLayer.mode import APPMODE
from helper import log_app_mode_transitions

class ModeManager:
    def __init__(self):
        self.mode = APPMODE.PRIMARY
        self.previous_mode = None

        self.allowed_transitions = {
            APPMODE.PRIMARY: [APPMODE.DEBUG],
            APPMODE.DEBUG: [APPMODE.PRIMARY]
        }

    def set_mode(self,new_mode):
        if new_mode == self.mode:
            return
        if new_mode in self.allowed_transitions:
            log_app_mode_transitions(self.mode,new_mode)
            self.set_previous_mode(self.mode)
            self.mode = new_mode
            print(self.get_mode())

    def get_mode(self):
        return f"APPMODE: {self.mode}"
    
    def is_mode(self,mode):
        return self.mode == mode

    def set_previous_mode(self,mode):
        self.previous_mode = mode