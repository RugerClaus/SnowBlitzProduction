from core.ui.composables.form import Form
from core.ui.widgets.textbox import TextBox
from core.ui.widgets.label import Label
from core.ui.widgets.query import Query
from core.engine.user import User
from core.util.colors import red


class LoginPage(Form):
    def __init__(self, system):
        super().__init__(system)

        self.user = User(system)

        self.query = Query(system, "Please enter your username or password")
        self.add_child(self.query)

        self.username_label = Label(system, "Username:", (0.37, 0.3))
        self.username_box = TextBox(system, (0.5, 0.3))

        self.password_label = Label(system, "Password:", (0.37, 0.4))
        self.password_box = TextBox(system, (0.5, 0.4))

        self.password_box.is_password = True

        self.add_field("username", self.username_box)
        self.add_field("password", self.password_box)

        self.add_child(self.username_label)
        self.add_child(self.password_label)

        self.set_error_element(self.query)

        self.ui.set_active(self.username_box)

    def clear(self):
        
        self.get_field("username").box.clear()
        self.get_field("password").box.clear()

    def submit(self):

        username = self.get_field("username").get_return_string()
        password = self.get_field("password").get_return_string()

        self.clear_error()

        if not username:
            self.set_error("Username is required", red)
            return False

        if not password:
            self.set_error("Password is required", red)
            return False

        result = self.system.auth.login(username, password)

        if result["success"]:
            self.get_field("username").box.clear()
            self.get_field("password").box.clear()
            self.system.save.write_constant("username", username)
            return True

        self.set_error(result["message"],red)

        return False