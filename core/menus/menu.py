import pygame
import math
from core.menus.basemenu import BaseMenu
from core.menus.usercreator import UserCreator
from core.ui.button import Button
from helper import *
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.menus.credits import Credits

class Menu(BaseMenu):
    def __init__(self, developer_mode, window, sound, endless_callback, blitz_callback, tutorial_callback, quit_callback):
        self.developer_mode = developer_mode
        self.window = window
        self.sound = sound
        super().__init__(window, sound)
        self.endless_callback = endless_callback
        self.blitz_callback = blitz_callback
        self.tutorial_callback = tutorial_callback
        self.quit_callback = quit_callback
        self.state = MenuStateManager()
        self.credits = Credits(self.window)
        self.agreed_to_leaderboard = check_leaderboard_opt()
        self.user_creator = UserCreator(self.window,self.sound,self.state)

        self.title_image_original = self.window.load_image(asset("title"))
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()
        
        if self.agreed_to_leaderboard:
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()
        else:
            print(self.agreed_to_leaderboard)
            self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
            self.create_buttons()

        self.create_buttons()
        self.rescale_assets()

    def rescale_assets(self):
        window_w, window_h = self.window.get_size()
        new_title_width = int(window_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = pygame.transform.scale(self.title_image_original, (new_title_width, new_title_height))
        self.title_rect = self.title_image.get_rect(center=(window_w // 2, int(window_h * 0.2)))
        self.credits.rescale()

    def create_buttons(self):
        window_w, window_h = self.window.get_size()
        btn_width, btn_height = window_w // 4.5, 70
        spacing = btn_height * 1.2
        start_y = window_h // 4 + window_h // 7
        center_x = window_w // 2

        if self.state.is_state(MENUSTATE.ROOT):
            self.buttons = [
                Button(self.window, "Endless Mode", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.endless_callback),
                Button(self.window, "Blitz Mode", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.blitz_callback),
                Button(self.window, "Tutorial", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), (128, 128, 128), self.tutorial_callback),
                Button(self.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), (128, 0, 200), self.go_to_settings),
                Button(self.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), (255, 0, 80), self.quit_callback),
                Button(self.window, "Credits", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.credits_callback),
                Button(self.window, "Leaderboard", window_w // 8, window_h - 100, 275, btn_height,
                    (255, 255, 255), (255, 0, 80), self.view_leaderboard),
            ]
        elif self.state.is_state(MENUSTATE.SETTINGS):
            if self.developer_mode.is_state(DEVELOPER_MODE.ON):
                self.buttons = [
                    Button(self.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.audio_settings),
                    Button(self.window, f"Developer Settings", center_x, start_y + spacing * 1, btn_width * 2, btn_height, (255, 255, 255), (128, 0, 200), self.developer_settings),
                    Button(self.window, "Back", center_x, start_y + spacing * 2, btn_width, btn_height,
                        (255, 255, 255), (255, 0, 80), self.back_to_root),
                ]
            else:
                self.buttons = [
                    Button(self.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.audio_settings),
                    Button(self.window, "Back", center_x, start_y + spacing * 1, btn_width, btn_height,
                        (255, 255, 255), (255, 0, 80), self.back_to_root),
                ]
        elif self.state.is_state(MENUSTATE.CREDITS):

            self.buttons = [
                Button(self.window, "Back", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.AUDIO):
            self.buttons = [
                Button(self.window, f"-", center_x - 200, self.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_down),
                Button(self.window, f"Music Vol: {int(self.sound.volume*10)}", center_x, self.window.get_height() // 2 - spacing, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.window, f"+", center_x + 200, self.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.volume_up),
                
                Button(self.window, f"-", center_x - 200, self.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.sfx_volume_down),
                Button(self.window, f"SFX Vol: {int(self.sound.sfx_volume*10)}", center_x, self.window.get_height() // 2 + spacing * 0.01, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.window, f"+", center_x + 200, self.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), (128, 0, 200), self.sound.sfx_volume_up),
                
                Button(self.window, f"Music:", center_x, self.window.get_height() // 2 + spacing * 1, 200, btn_height,
                    (255, 255, 255), (128, 0, 200), self.sound.toggle_music),
                Button(self.window, f"UI SFX:", center_x, self.window.get_height() // 2 + spacing * 2, 200, btn_height,
                    (255, 255, 255), (128, 0, 200), self.toggle_ui_sfx),
                Button(self.window, f"Game SFX:", center_x, self.window.get_height() // 2 + spacing * 3, 300, btn_height,
                    (255, 255, 255), (128, 0, 200), self.toggle_game_sfx),
                Button(self.window, "Back", center_x, self.window.get_height() // 2 + spacing * 4, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.go_to_settings)
            ]
        elif self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            if self.developer_mode.is_state(DEVELOPER_MODE.ON):
                self.buttons = [
                    Button(self.window, f"Yes", center_x - btn_width, self.window.get_height() // 2 + spacing * 0.4, 90, btn_height, (255, 255, 255), (128, 0, 200), self.leaderboard_opt_in_dev),
                    Button(self.window, f"No", center_x + btn_width, self.window.get_height() // 2 + spacing * 0.4, 80, btn_height, (255, 255, 255), (128, 0, 200), self.leaderboard_opt_out),
                ]
            else:
                self.buttons = [
                    Button(self.window, f"Yes", center_x - btn_width, self.window.get_height() // 2 + spacing * 0.4, 90, btn_height, (255, 255, 255), (128, 0, 200), self.leaderboard_opt_in),
                    Button(self.window, f"No", center_x + btn_width, self.window.get_height() // 2 + spacing * 0.4, 80, btn_height, (255, 255, 255), (128, 0, 200), self.leaderboard_opt_out),
                ]
        elif self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.buttons = [
                Button(self.window, f"Submit", center_x, self.window.get_height() // 2 + spacing * 0.4, btn_width, btn_height, (255, 255, 255), (128, 0, 200), self.submit_username),
            ]
    
        elif self.state.is_state(MENUSTATE.LEADERBOARDVIEWER):
            self.buttons = [
                Button(self.window, "Back", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.buttons = [
                Button(self.window, "Reset Username", center_x, self.window.get_height() // 2 - spacing, btn_width + 50, btn_height,
                    (255, 255, 255), (255, 0, 80), self.reset_username),
                Button(self.window, "Change Leaderboard Opt-in Status", center_x, self.window.get_height() // 2, btn_width * 2 + 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.change_opt_in),
                Button(self.window, "Back", center_x, self.window.get_height() // 2 + spacing, 150, btn_height,
                    (255, 255, 255), (255, 0, 80), self.go_to_settings),
            ]

    def developer_settings(self):
        self.state.set_state(MENUSTATE.DEVELOPERSETTINGS)
        self.create_buttons()
    
    def change_opt_in(self):
        self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
        self.create_buttons()

    def reset_username(self):
        delete_constant_file('username')
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()

    def submit_username(self):
        username = self.user_creator.text_box.get_return_string()
        if len(username) > 5:
            self.user_creator.submit()
            self.set_query(None)
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()
        else:
            self.set_query("Username must be at least 6 characters")

    def leaderboard_opt_in(self):
        write_constant_to_file('leaderboard_opt_in','YES')
        self.query = None
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()
    
    def leaderboard_opt_in_dev(self):
        if read_constant_from_file('username') == None:
            write_constant_to_file('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.CREATEUSERNAME)
            self.create_buttons()
        else:
            write_constant_to_file('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()

    
    def leaderboard_opt_out(self):
        write_constant_to_file('leaderboard_opt_in', 'NO')
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()
        self.query = None
        
    def view_leaderboard(self):
        self.state.set_state(MENUSTATE.LEADERBOARDVIEWER)
        self.create_buttons()

    def credits_callback(self):
        self.state.set_state(MENUSTATE.CREDITS)
        self.create_buttons()

    def audio_settings(self):
        self.state.set_state(MENUSTATE.AUDIO)
        self.create_buttons()

    def back_to_root(self):
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()
    
    def go_to_settings(self):
        self.state.set_state(MENUSTATE.SETTINGS)
        self.create_buttons()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == pygame.VIDEORESIZE:
            self.scale()
        self.user_creator.handle_event(event)

    def scale(self):
        self.rescale_assets()
        self.create_buttons()

    def draw(self):
        t = self.window.get_current_time() / 1000
        pulse = (math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.window.fill(fade_color)

        if self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            self.set_title(None)
            self.set_query("DO YOU AGREE TO HAVE YOUR SCORES POSTED ON A GLOBAL LEADERBOARD?")

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(mouse_pos)
            button.get_sound_engine(self.sound)

        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.set_title(None)
            self.user_creator.draw()

        if self.state.is_state(MENUSTATE.ROOT):
            self.set_title(None)
            self.window.blit(self.title_image, self.title_rect)

        if self.state.is_state(MENUSTATE.SETTINGS):
            self.set_title("SETTINGS")
        
        if self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.set_title('DEVELOPER SETTINGS')

        if self.state.is_state(MENUSTATE.CREDITS):
            self.credits.draw()

        if self.state.is_state(MENUSTATE.AUDIO):
            self.set_title("AUDIO SETTINGS")
        
        self.draw_title()