from core.guts.user import User
from core.ui.textbox import TextBox
from core.ui.UIManager import UIManager
from core.ui.label import Label

class UserCreator:
    def __init__(self, system):
        self.system = system
        self.user = User(system)

        self.username_label = Label(system, "Username:", 0.37, 0.3)
        self.username_box = TextBox(system, 0.5, 0.3)

        self.password_label = Label(system, "Password:", 0.37, 0.4)
        self.password_box = TextBox(system, 0.5, 0.4)
        self.password_box.is_password = True

        self.confirm_password_label = Label(system,"Password", 0.37,0.5)
        self.confirm_password_box = TextBox(system, 0.5,0.5)
        self.confirm_password_box.is_password = True

        self.ui = UIManager(system)

        self.ui.add(self.username_label)
        self.ui.add(self.username_box)
        self.ui.add(self.password_label)
        self.ui.add(self.password_box)
        self.ui.add(self.confirm_password_label)
        self.ui.add(self.confirm_password_box)

        self.ui.set_active(self.username_box)

        self.error = None

    def handle_event(self, event):
        self.ui.handle_event(event)

    def scale(self):
        self.ui.scale()

    def draw(self):
        self.ui.draw()

    def submit(self):
        username = self.username_box.get_return_string()
        password = self.password_box.get_return_string()
        confirm_password = self.confirm_password_box.get_return_string()

        self.error = None

        if not username:
            self.error = "Username is required"
            return False

        if len(username) < 5:
            self.error = "Username must be more than 5 characters"
            return False

        if password != confirm_password:
            self.error = "Passwords do not match"
            return False

        result = self.system.auth.register(
            username,
            password
        )

        if result["success"]:
            self.username_box.box.clear()
            self.password_box.box.clear()
            self.confirm_password_box.box.clear()

            # Update the actual system user here if needed
            self.system.user.username = username

            return True

        self.error = result["message"]
        return False