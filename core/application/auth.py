class Auth:
    def __init__(self,app):
        self.application = app
        self.system = app.system
        self.error_timeout = 0

    def login_user(self):
        form = self.application.distant_realms.ui_controller.get_active_ui()

        for key,value in form.fields.items():
            if key == "username":
                username = value.get_return_string()
            if key == "password":
                password = value.get_return_string()

        if not username:

            for element in form.children:
                if element.id == "username":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Username is required!"
            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        if not password:
        
            for element in form.children:
                if element.id == "password":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Password is required!"
            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        result = self.application.auth.login(username,password)
        
        if result["success"]:
            self.application.distant_realms.ui_controller.show_ui("main_menu")

        for element in form.children:
            if element.id =="username" or element.id == "password":
                element.error_back()
            if element.id == "errormsg":
                element.text = "Bad Username or Password!"
        self.error_timeout = self.system.time.get_current_time() + 2000

    def sign_up_new_user(self):
        form = self.application.distant_realms.ui_controller.get_active_ui()

        for key, value in form.fields.items():
            if key == "username":
                username = value.get_return_string()

            if key == "password":
                password = value.get_return_string()

            if key == "confirm_password":
                confirm_password = value.get_return_string()

        if not username:

            for element in form.children:
                if element.id == "username":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Username is required!"

            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        if len(username) < 5:

            for element in form.children:
                if element.id == "username":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Username must be more than 5 characters!"

            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        if not password:

            for element in form.children:
                if element.id == "password":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Password is required!"

            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        if len(password) < 8:

            for element in form.children:
                if element.id == "password":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Password must be at least 8 characters!"

            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        if password != confirm_password:

            for element in form.children:
                if element.id == "confirm_password":
                    element.error_back()

                if element.id == "errormsg":
                    element.text = "Passwords do not match!"

            self.error_timeout = self.system.time.get_current_time() + 2000
            return False

        result = self.application.auth.register(username, password)

        if result["success"]:
            for element in form.children:
                if element.id == "username":
                    element.clear_error()
                elif element.id == "password":
                    element.clear_error()
                elif element.id == "confirm_password":
                    element.clear_error()

            self.application.distant_realms.ui_controller.show_ui("main_menu")
            return True

        for element in form.children:
            if element.id == "errormsg":
                element.text = result["message"]

        self.error_timeout = self.system.time.get_current_time() + 2000
        return False

    def handle_event(self,event,command=None):
        activeui = self.application.distant_realms.ui_controller.active_name

        if event.type == self.system.input.keydown():
            if event.key == self.system.input.keys.return_key():
                if activeui == "login_form":
                    self.login_user()

                if activeui == "sign_up_form":
                    self.sign_up_new_user()

    def update(self):
        if self.error_timeout:
            if self.system.time.get_current_time() >= self.error_timeout:
                self.clear_error()
                self.error_timeout = 0

    def clear_error(self):
        form = self.application.distant_realms.ui_controller.get_active_ui()

        for element in form.children:
            if element.id == "errormsg":
                element.text = ""
            elif element.id == "username" or element.id == "password":
                element.clear_error()

    def toggle_pass(self):
        form = self.application.distant_realms.ui_controller.get_active_ui()

        for element in form.children:

            if element.id == "password":
                fieldispass = element.is_password
                element.is_password = not element.is_password

            if element.id == "show_password_button":
                if fieldispass:
                    element.text = "SHOW"
                else:
                    element.text = "HIDE"