import threading
from .endpoints import CREATE_SESSION
from core.engine.network.system_endpoints import API_KEY,VERSION
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE
from core.application.network.leaderboard import Leaderboard
from core.state.ApplicationLayer.Session.state import ONLINE_SESSION_STATE
from core.state.ApplicationLayer.Session.statemanager import OnlineSessionStateManager
class Session:
    def __init__(self, system):
        self.system = system
        self.state = OnlineSessionStateManager()
        self.sessionToken = None

        self.session_thread = None
        self.session_response = None

    def start_online_session(self):

        if self.session_thread and self.session_thread.is_alive():
            return False

        self.state.set_state(ONLINE_SESSION_STATE.STARTING)

        self.session_thread = threading.Thread(
            target=self._create_session_request,
            daemon=True
        )

        self.session_thread.start()

        return True
    
    def _create_session_request(self):

        app_pass = self.system.load.read_constant("clientAppPassword")
        cid = self.system.load.read_constant("clientID")

        response = self.system.network.post(
            CREATE_SESSION,
            {
                "key": API_KEY,
                "clientID": cid,
                "clientAppPassword": app_pass,
                "version": VERSION
            }
        )

        self.session_response = response

    def update(self):

        if self.state.is_state(ONLINE_SESSION_STATE.STARTING):

            if self.session_response is None:
                return

            response = self.session_response
            self.session_response = None


            if not response["success"]:

                message = response.get(
                    "message",
                    "Unknown server error"
                )

                self.system.app_inspector["OnlineSession"] = False

                if message == "Client version is outdated":
                    self.system.app_inspector["OnlineSessionError"] = {
                        "type": "VERSION_OUTDATED",
                        "minimumVersion": response.get("minimumVersion")
                    }
                self.state.set_state(ONLINE_SESSION_STATE.INACTIVE)
                return


            data = response.get("data")

            if not data or "sessionToken" not in data:

                self.state.set_state(ONLINE_SESSION_STATE.INACTIVE)
                return


            self.sessionToken = data["sessionToken"]

            self.state.set_state(
                ONLINE_SESSION_STATE.ACTIVE
            )

            self.system.app_inspector["OnlineSession"] = True
        
    def submit_score(self, score):
        
        if not self.state.is_state(ONLINE_SESSION_STATE.ACTIVE):
            return False

        leaderboard = Leaderboard(self.system)

        submission = leaderboard.submit(score,self.sessionToken)

        if submission:
            self.end_online_session()

    def end_online_session(self):
        self.state.set_state(ONLINE_SESSION_STATE.INACTIVE)
        self.system.app_inspector["OnlineSession"] = False
        self.sessionToken = None

    def clean_up_states(self):
        self.system.clean_up_states([self.state.state])