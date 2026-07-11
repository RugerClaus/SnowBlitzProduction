from core.application.network.endpoints import LOGIN,REGISTER


class Authentication:

    def __init__(self, system):
        self.system = system
        self.network = system.network

        print("REGISTER ENDPOINT:", REGISTER)
        print("LOGIN ENDPOINT:", LOGIN)

    def register(self, username, password):

        response = self.network.post(
            REGISTER,
            {
                "username": username,
                "password": password
            }
        )

        if not response["success"]:
            return response

        data = response["data"]

        if data.get("message") == "Username already exists":
            return {
                "success": False,
                "message": "Username already exists."
            }

        self.system.save.write_constant(
            "username",
            username
        )

        self.system.save.write_constant(
            "clientAPIKey",
            data["clientAPIKey"]
        )

        return {
            "success": True
        }

    def login(self, username, password):

        response = self.network.post(
            LOGIN,
            {
                "username": username,
                "password": password
            }
        )

        if not response["success"]:
            return response

        data = response["data"]

        if data.get("message") == "Incorrect username or password":

            return {
                "success": False,
                "message": data["message"]
            }

        self.system.state_monitor["ClientConnected"] = True

        return {
            "success": True,
            "data": data
        }

    def auto_login(self):

        username = self.system.load.read_constant("username")
        key = self.system.load.read_constant("clientAPIKey")

        if not username or not key:
            return {
                "success": False
            }

        return self.network.post(
            LOGIN,
            {
                "username": username,
                "clientAPIKey": key
            }
        )