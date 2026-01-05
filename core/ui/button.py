from core.ui.font import FontEngine

from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE

class Button:
    def __init__(self, window, text, x, y, width, height, text_unhovered_color, text_hovered_color, action=None,active=True):
        self.window = window
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = FontEngine("button").font
        self.action = action
        self.active = active
        self.text_unhovered_color = text_unhovered_color
        self.text_hovered_color = text_hovered_color
        self.color = (0, 0, 0)

        self.surface = self.window.make_surface(self.width, self.height)
        self.rect = self.surface.get_rect()
        self.sound = None

    def get_sound_engine(self,sound):
        self.sound = sound

    def draw(self, mouse_pos):
        self.surface.fill((0, 0, 0),0)

        if self.rect.collidepoint(mouse_pos):
            text_color = self.text_hovered_color
            print(self.rect.topleft)
        else:
            text_color = self.text_unhovered_color

        self.text_surface = self.font.render(self.text, True, text_color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.window.draw_rect(self.surface, (0, 0, 0), self.surface.get_rect(), border_radius=8)
        self.window.draw_rect(self.surface, (255, 0, 0), self.surface.get_rect(), width=2, border_radius=8)
        self.window.blit(self.surface, self.rect.topleft)
        self.window.blit(self.text_surface, self.text_rect)

        

    def is_clicked(self, mouse_pos, mouse_click):
        
        if self.active and self.rect.collidepoint(mouse_pos) and mouse_click:
            if self.action:
                if self.sound.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
                    self.sound.play_ui_sfx('button_clicked')
                else:
                    print(f'interface sfx is disabled.{self.sound.interface_sfx_state.get_state()}')
                self.action()
            if not self.action:
                self.action = None

    def get_text_height(self):
        return self.text_rect.height
    
    def set_new_text(self,new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.text_unhovered_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)