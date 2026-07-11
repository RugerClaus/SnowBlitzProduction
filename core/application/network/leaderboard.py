from .endpoints import LEADERBOARD, UPDATE_SCORE
from systemlogging import log_error, log_event


class Leaderboard:
    def __init__(self, system):
        self.system = system
        self.leaderboardURL = LEADERBOARD
        self.submit_url = UPDATE_SCORE

        if not self.leaderboardURL:
            log_error("Leaderboard URL not set in config")

        if not self.submit_url:
            log_error("Leaderboard submission URL not set in config")

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

    def submit(self, score):
        if score is None:
            log_error("Unable to submit empty score")
            return False

        if not self.submit_url:
            log_event(
                "No leaderboard submission endpoint configured. "
                "Score was not submitted."
            )
            return False

        username = self.system.user.username

        if not username:
            log_error(
                "Unable to submit score without username"
            )
            return False

        data = {
            "username": username,
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
            f"Submitted leaderboard score for {username}: {score}"
        )

        return True