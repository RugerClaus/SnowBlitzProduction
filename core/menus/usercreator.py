from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.network.user import User

from core.ui.textbox import TextBox
from helper import *

class UserCreator:
    def __init__(self,window,sound,state,input):
        self.window = window
        self.sound = sound
        self.state = state
        self.input = input
        self.user = User()
        self.text_box = TextBox(self.window,self.sound,self.input)
    
    def handle_event(self,event):
        self.text_box.handle_event(event)

    def scale(self):
        self.text_box.scale()

    def draw(self):
        self.text_box.draw()
    
    def submit(self):
        username = self.text_box.get_return_string()
        if username is not None:
            print('writing username file')
            write_constant_to_file('username',str(username))
            self.text_box.box.clear()
            self.user.send_username_to_api()