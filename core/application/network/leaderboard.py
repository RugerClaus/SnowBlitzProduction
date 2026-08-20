from .endpoints import LEADERBOARD, UPDATE_SCORE
from core.engine.network.system_endpoints import API_KEY
from systemlogging import log_error, log_event, log_warning
from core.engine.user import User


class Leaderboard:
    def __init__(self, system):
        self.system = system
        self.leaderboardURL = LEADERBOARD
        self.submit_url = UPDATE_SCORE

        if not self.leaderboardURL:
            log_error("Leaderboard URL not set in config")

        if not self.submit_url:
            log_error("Leaderboard submission URL not set in config")

    def get_logged_in_user_score(self):
        if not self.leaderboardURL:
            log_error("Unable to fetch leaderboard: No endpoint configured")
            return ("error", "Missing leaderboard endpoint")

        response = self.system.network.get(
            self.leaderboardURL
        )

        if not response["success"]:
            log_error(
                f"Failed to fetch leaderboard: {response['message']}"
            )
            return ("error", response["message"])

        log_event("Fetched leaderboard data.")

        for user in response["data"]:
            local_user = User(self.system)
            if user["username"] == local_user.username:
                local_user.high_score = user["score"]

    def fetch_leaderboard(self):
        if not self.leaderboardURL:
            log_error("Unable to fetch leaderboard: No endpoint configured")
            return ("error", "Missing leaderboard endpoint")

        response = self.system.network.get(
            self.leaderboardURL
        )

        if not response["success"]:
            log_error(
                f"Failed to fetch leaderboard: {response['message']}"
            )
            return ("error", response["message"])

        log_event("Fetched leaderboard data.")
        


        return ("success", response["data"])

    def submit(self, score,session_token):

        if score is None:
            log_error("Unable to submit empty score")
            return False
        
        if session_token is None:
            log_error("Unable to update score without valid session token")
            return False

        if not self.submit_url:
            log_event(
                "No leaderboard submission endpoint configured. "
                "Score was not submitted."
            )
            return False

        app_password = self.system.persistence.load.read_constant("clientAppPassword")

        if not app_password:
            log_error("Missing application password, reauthenticate your client")
            return False
        
        if User(self.system).username == "Player":
            log_warning("User not Logged in, cannot send score to server")
            return False

        data = {
            "key": API_KEY,
            "clientAppPassword": app_password,
            "sessionToken": session_token,
            "score": int(score)
        }

        response = self.system.network.post(
            self.submit_url,
            data
        )

        if not response["success"]:
            log_error(
                f"Leaderboard submission failed: "
                f"{response['message']}"
            )
            return False

        log_event(
            f"Submitted leaderboard score for {self.system.user.username}: {score}"
        )

        return True
    
