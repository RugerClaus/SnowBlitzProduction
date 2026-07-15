from core.ui.form import Form
from core.ui.textbox import TextBox
from core.ui.label import Label
from core.ui.query import Query
from core.guts.user import User
from core.util.colors import red


class UserCreator(Form):
    def __init__(self, system):
        super().__init__(system)

        self.user = User(system)

        self.query = Query(system,"Please enter a username and create a password:")

        self.add_child(self.query)

        self.username_label = Label(system,"Username:",(0.37,0.3))
        self.username_box = TextBox(system,(0.5,0.3))

        self.password_label = Label(system,"Password:",(0.37,0.4))
        self.password_box = TextBox(system,(0.5,0.4))

        self.password_box.is_password = True

        self.confirm_password_label = Label(system,"Confirm Password:",(0.37,0.5))
        self.confirm_password_box = TextBox(system,(0.5,0.5))

        self.confirm_password_box.is_password = True


        self.add_field("username", self.username_box)
        self.add_field("password", self.password_box)
        self.add_field("confirm_password", self.confirm_password_box)


        self.add_child(self.username_label)
        self.add_child(self.password_label)
        self.add_child(self.confirm_password_label)


        self.set_error_element(self.query)

        self.ui.set_active(self.username_box)

    def submit(self):

        username = self.get_field("username").get_return_string()
        password = self.get_field("password").get_return_string()
        confirm = self.get_field("confirm_password").get_return_string()

        self.clear_error()

        if not username:
            self.set_error(
                "Username is required",
                red
            )
            return False

        if len(username) < 5:
            self.set_error(
                "Username must be more than 5 characters",
                red
            )
            return False

        if len(password) < 8:
            self.set_error(
                "Password must be at least 8 characters",
                red
            )
            return False

        if password != confirm:
            self.set_error(
                "Passwords do not match",
                red
            )
            return False


        result = self.system.auth.register(
            username,
            password
        )


        if result["success"]:
            self.get_field("username").box.clear()
            self.get_field("password").box.clear()
            self.get_field("confirm_password").box.clear()

            self.system.save.write_constant(
                "username",
                username
            )

            return True


        self.set_error(result["message"])
        return False