import requests,json

from helper import *
class User:
    def __init__(self):
        self.setusernameURL = 'http://localhost:8000/createUsername.php'
        self.setuserhighscoreURL = 'http://localhost:8000/setUserHighScore.php'

    def get_username(self):
        username = read_constant_from_file('username')
        if username is not None:
            return username
        else:
            return None

    def get_high_score(self):
        high_score = read_constant_from_file('high_score')
        if high_score is not None:
            return high_score
        else:
            return None

    def send_username_to_api(self):
        username = self.get_username()
        if username:
            data = {"username": str(username)}
            try:
                response = requests.post(self.setusernameURL, json=data)
                if response.status_code == 200:
                    log_event(f"Username added to global database. Status: {str(response.status_code)}; Response: {response.json()}")
                else:
                    log_error(f"Failed to create username in global database. Status: {str(response.status_code)}; Response: {response.text}")
            except requests.exceptions.RequestException as e:
                log_error(f"Network error while sending username: {e} Status: {response.status_code}; Response: {response.text}")
        else:
            log_error("Username is blank or invalid.")
    
    def send_high_score_to_api(self):
        high_score = self.get_high_score()
        username = self.get_username()

        if high_score and username:
            data = {
                "username": str(username),
                "score": int(high_score)
            }
            try:
                print("sending score to db")
                response = requests.post(self.setuserhighscoreURL, json=data)
                if response.status_code == 200:
                    log_event(f"Highscore added for {username}. Status: {response.status_code}; Response: {response.json()}")
                else:
                    log_error(f"Failed to send highscore for {username}. Status: {response.status_code}; Response: {response.text}")
            except requests.exceptions.RequestException as e:
                log_error(f"Network error while sending high score: {e} Status: {response.status_code}; Response: {response.text}")
        else:
            log_error(f"Highscore or Username is missing. Highscore: {high_score}, Username: {username}")