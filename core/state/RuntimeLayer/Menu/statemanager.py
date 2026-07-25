from core.state.RuntimeLayer.Menu.state import MENUSTATE
from core.state.basestatemanager import BaseStateManager
from systemlogging import log_state_transition

class MenuStateManager(BaseStateManager):
    def __init__(self):

        allowed_transitions = {
            MENUSTATE.CREATEACCOUNT: [MENUSTATE.ROOT,MENUSTATE.CHANGELOG,MENUSTATE.LOGIN,MENUSTATE.SETTINGS],
            MENUSTATE.ROOT: [MENUSTATE.SETTINGS,MENUSTATE.CREDITS,MENUSTATE.CHANGELOG,MENUSTATE.CREATEACCOUNT,MENUSTATE.LEADERBOARDVIEWER,MENUSTATE.LEADERBOARDOPTIN],
            MENUSTATE.SETTINGS: [MENUSTATE.ROOT,MENUSTATE.AUDIO,MENUSTATE.DEVELOPERSETTINGS,MENUSTATE.LOGIN,MENUSTATE.CREATEACCOUNT,MENUSTATE.LEADERBOARDOPTIN],
            MENUSTATE.DEVELOPERSETTINGS: [MENUSTATE.SETTINGS,MENUSTATE.CREATEACCOUNT],
            MENUSTATE.AUDIO: [MENUSTATE.SETTINGS],
            MENUSTATE.CREDITS: [MENUSTATE.ROOT],
            MENUSTATE.CHANGELOG: [MENUSTATE.ROOT,MENUSTATE.CREATEACCOUNT,MENUSTATE.LEADERBOARDOPTIN],
            MENUSTATE.LEADERBOARDVIEWER: [MENUSTATE.ROOT],
            MENUSTATE.LEADERBOARDOPTIN: [MENUSTATE.CREATEACCOUNT,MENUSTATE.ROOT],
            MENUSTATE.LOGIN: [MENUSTATE.ROOT,MENUSTATE.SETTINGS]

        }

        super().__init__(
                initial_state=MENUSTATE.ROOT,
                allowed_transitions=allowed_transitions,
                log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
                state_name="MENUSTATE",
                type="RUNTIME"
            )
