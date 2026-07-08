import requests

class Network:
    def __init__(self):
        pass

    def check_network_status(self):
        try:
            response = requests.get("https://snowblitz.net", timeout=5)
            if response.status_code is not None:
                return True
            else:
                return False
        except requests.ConnectionError:
            return False