from core.ui.font import FontEngine
from core.guts.input.inputmanager import InputManager

from helper import *

class TextBox:
    def __init__(self,window,sound):
        self.window = window
        self.sound = sound
        self.input = InputManager(self.window)
        self.font = FontEngine(30).font
        self.bounding_box = self.window.make_surface(275,100)
        self.bounding_box_rect = self.bounding_box.get_rect(center=(self.window.get_width()//2,self.window.get_height()//3))
        self.bounding_box.fill((0,0,0))
        self.text_box = self.window.make_surface(250,50)
        self.text_box_rect = self.text_box.get_rect(center=self.bounding_box_rect.center)
        self.text_box.fill((255,255,255))
        self.string = None
        self.box = [' ']
    
    def handle_event(self,event):
        key = self.input.handle_event(event,True)
        if key is not None:
            self.add_key_to_box(key)
            if self.input.get_key_name(key) == 'backspace' and len(self.box) > 0:
                self.delete_key()

    def add_key_to_box(self,key):
        if len(self.box) < 21:
            current_key = self.input.get_key_name(key)
            allowed_keys = "asdfghjklzxcvbnmqwertyuiopASDFGHJKLZXCVBNMQWERTYUIOP123456789"
            if current_key in allowed_keys:
                self.box.append(self.input.get_key_name(key))
            if current_key == 'space':
                self.box.append(" ")
    
    def get_return_string(self):
        return ''.join(self.box).strip()

    def delete_key(self):
        self.box.pop(-1)

    def draw(self):
        if len(self.box) > 0:
            text = ''.join(self.box)
        else:
            text = ''
        
        surf = self.font.render(text,False,(0,0,0))
        rect = surf.get_rect(center=self.text_box_rect.center)
        self.window.blit(self.bounding_box,self.bounding_box_rect)
        self.window.blit(self.text_box,self.text_box_rect)
        self.window.blit(surf,rect)