from core.state.ApplicationLayer.Mechanics.Season.state import SEASON_STATE
from core.state.ApplicationLayer.Mechanics.Season.statemanager import SeasonStateManager

class Season:
    def __init__(self,dayc):
        self.state = SeasonStateManager()
        self.day = dayc.day

    def winter(self):
        self.min = -20
        self.max = 2
    
    def spring(self):
        self.min = 0
        self.max = 20

    def summer(self):
        self.min = 22
        self.max = 38

    def autumn(self):
        self.min = 5
        self.max = 21

    def update(self):
        if self.state.is_state(SEASON_STATE.WINTER):
            self.winter()
        elif self.state.is_state(SEASON_STATE.SPRING):
            self.spring()
        elif self.state.is_state(SEASON_STATE.SUMMER):
            self.summer()
        elif self.state.is_state(SEASON_STATE.AUTUMN):
            self.autumn()

    def update_season(self):
        if self.day < 25:
            self.state.set_state(SEASON_STATE.WINTER)
        elif self.day < 50:
            self.state.set_state(SEASON_STATE.SPRING)
        elif self.day < 75:
            self.state.set_state(SEASON_STATE.SUMMER)
        elif self.day <= 100:
            self.state.set_state(SEASON_STATE.AUTUMN)