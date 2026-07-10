from core.network.user import User
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

        self.ui = UIManager(system)

        self.ui.add(self.username_label)
        self.ui.add(self.username_box)
        # self.ui.add(self.password_label)
        # self.ui.add(self.password_box)

        self.ui.set_active(self.username_box)

    def handle_event(self, event):
        self.ui.handle_event(event)

    def scale(self):
        self.ui.scale()

    def draw(self):
        self.ui.draw()

    def submit(self):
        username = self.username_box.get_return_string()

        if username:
            self.system.save.write_constant('username', username)
            self.username_box.box.clear()
            self.user.send_username_to_api()