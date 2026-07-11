import webbrowser
from core.menus.basemenu import BaseMenu
from core.menus.usercreator import UserCreator
from core.ui.button import Button
from helper import asset
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.Menu.state import MENUSTATE
from core.state.GameLayer.GameMode.state import GAME_MODE
from core.state.ApplicationLayer.Menu.statemanager import MenuStateManager
from core.menus.credits import Credits
from core.menus.leaderboardviewer import LeaderboardViewer
from core.state.ApplicationLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.guts.network.update import Update
from core.state.ApplicationLayer.NetworkLayer.Update.state import UPDATE_STATE

from core.menus.changelog import ChangeLog

class Menu(BaseMenu):
    def __init__(self,system):
        self.system = system
        super().__init__(system)
        self.state = MenuStateManager()
        self.credits = Credits(system)
        self.agreed_to_leaderboard = self.check_leaderboard_opt()
        self.recently_updated = self.check_recently_updated()
        self.user_creator = UserCreator(system)
        self.leaderboard = LeaderboardViewer(system,self.state,self.back_to_root)
        self.updater = Update()
        self.change_log = ChangeLog(system)

        self.title_image_original = self.system.window.load_image(asset("title"))
        self.title_image = self.title_image_original
        self.title_rect = self.title_image.get_rect()
        

        if self.agreed_to_leaderboard:
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()
        else:
            self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
            self.create_buttons()
        
        recently_updated_file = self.system.load.read_envar('recentlyupdated')
        if self.state.is_state(MENUSTATE.ROOT):
            if self.recently_updated:
                if recently_updated_file == "false":
                    self.state.set_state(MENUSTATE.ROOT)
                if recently_updated_file == "true":
                    self.state.set_state(MENUSTATE.CHANGELOG)
                    self.create_buttons()

        self.create_buttons()
        self.rescale_assets()
        
    def check_leaderboard_opt(self):
        opt_in = self.system.load.read_constant('leaderboard_opt_in')
        if opt_in is not None:
            return True
        else:
            return False

    def check_recently_updated(self):
        updated = self.system.load.read_envar('recentlyupdated')
        if updated is not None:
            return True
        else:
            return False

    def rescale_assets(self):
        window_w, window_h = self.system.window.get_size()
        new_title_width = int(window_w * 0.5)
        scale_factor = new_title_width / self.title_image_original.get_width()
        new_title_height = int(self.title_image_original.get_height() * scale_factor)
        self.title_image = self.system.window.transform_scale(self.title_image_original, new_title_width, new_title_height)
        self.title_rect = self.title_image.get_rect(center=(window_w // 2, int(window_h * 0.2)))
        self.credits.rescale()
        self.user_creator.scale()

    def create_buttons(self):
        
        window_w, window_h = self.system.window.get_size()
        btn_width, btn_height = window_w // 3.6, 70
        spacing = btn_height * 1.2
        start_y = window_h // 4 + window_h // 7
        center_x = window_w // 2
        

        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.buttons = [
                Button(self.system.sound, self.system.window, "Endless Mode", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.endless),
                Button(self.system.sound, self.system.window, "Blitz Mode", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), self.button_action_false_color, self.blitz,False),
                Button(self.system.sound, self.system.window, "Tutorial", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.tutorial),
                Button(self.system.sound, self.system.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
                Button(self.system.sound, self.system.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.quit),
                Button(self.system.sound, self.system.window, "Credits", window_w - window_w // 8, window_h - 100, 200, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.credits_callback),
                Button(self.system.sound, self.system.window, "Our Discord", window_w - window_w // 8 - 50, window_h - 200, 300, btn_height,
                    (255, 0, 0), self.button_action_true_color, self.discord_invite, True, (50,205,50)),
                Button(self.system.sound, self.system.window, "Website", window_w // 8 + 50, window_h - 200, 200, btn_height,
                    (255, 0, 0), self.button_action_true_color, self.open_website,True,(50,205,50)),
                Button(self.system.sound, self.system.window, "Leaderboard", window_w // 8 + 50, window_h - 100, window_w // 4 if window_w < 800 else 300, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.view_leaderboard),
            ]
        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.buttons = [
                Button(self.system.sound, self.system.window, "Endless Mode", center_x, start_y, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.endless),
                Button(self.system.sound, self.system.window, "Blitz Mode", center_x, start_y + spacing, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.blitz),
                Button(self.system.sound, self.system.window, "Tutorial", center_x, start_y + spacing * 2, btn_width, btn_height,
                    (255, 255, 255), self.button_action_false_color, self.tutorial),
                Button(self.system.sound, self.system.window, "Settings", center_x, start_y + spacing * 3, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
                Button(self.system.sound, self.system.window, "Quit", center_x, start_y + spacing * 4, btn_width, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.quit),
                Button(self.system.sound, self.system.window, "Update!", window_w - window_w // 8, window_h - 300, 220, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.updater.start, True, (255, 165, 0)),
                Button(self.system.sound, self.system.window, "Our Discord", window_w - window_w // 8 - 50, window_h - 200, 300, btn_height,
                    (255, 0, 0), self.button_action_true_color, self.discord_invite, True, (50,205,50)),
                Button(self.system.sound, self.system.window, "Credits", window_w - window_w // 8, window_h - 100, 200, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.credits_callback),
                Button(self.system.sound, self.system.window, "Website", window_w // 8 + 50, window_h - 200, 200, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.open_website,True,(50,205,50)),
                Button(self.system.sound, self.system.window, "Leaderboard", window_w // 8 + 50, window_h - 100, window_w // 4 if window_w < 800 else 300, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.view_leaderboard),
            ]
        elif self.state.is_state(MENUSTATE.SETTINGS):
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.audio_settings),
                    Button(self.system.sound, self.system.window, f"Developer Settings", center_x, start_y + spacing * 1, btn_width * 2, btn_height, (255, 255, 255), self.button_action_true_color, self.developer_settings),
                    Button(self.system.sound, self.system.window, "Back", center_x, start_y + spacing * 2, btn_width, btn_height,
                        (255, 255, 255), self.button_action_true_color, self.back_to_root),
                ]
            else:
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Audio", center_x, start_y, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.audio_settings),
                    Button(self.system.sound, self.system.window, "Back", center_x, start_y + spacing * 1, btn_width, btn_height,
                        (255, 255, 255), self.button_action_true_color, self.back_to_root),
                ]
        elif self.state.is_state(MENUSTATE.CREDITS):

            self.buttons = [
                Button(self.system.sound, self.system.window, "Back", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.CHANGELOG):

            self.buttons = [
                Button(self.system.sound, self.system.window, "Go To Menu", window_w - window_w // 8 - 50, window_h - 100, 300, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.back_to_root_changelog),
            ]
            
        elif self.state.is_state(MENUSTATE.AUDIO):
            self.buttons = [
                Button(self.system.sound, self.system.window, f"-", center_x - 200, self.system.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.volume_down),
                Button(self.system.sound, self.system.window, f"Music Vol: {int(self.system.sound.volume*10)}", center_x, self.system.window.get_height() // 2 - spacing, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.system.sound, self.system.window, f"+", center_x + 200, self.system.window.get_height() // 2 - spacing, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.volume_up),
                
                Button(self.system.sound, self.system.window, f"-", center_x - 200, self.system.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.sfx_volume_down),
                Button(self.system.sound, self.system.window, f"SFX Vol: {int(self.system.sound.sfx_volume*10)}", center_x, self.system.window.get_height() // 2 + spacing * 0.01, 0, btn_height, (255, 255, 255), (255,255,255), None,False),
                Button(self.system.sound, self.system.window, f"+", center_x + 200, self.system.window.get_height() // 2 + spacing * 0.01, 50, btn_height, (255, 255, 255), self.button_action_true_color, self.system.sound.sfx_volume_up),
                
                Button(self.system.sound, self.system.window, f"Music:", center_x, self.system.window.get_height() // 2 + spacing * 1, 240, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.system.sound.toggle_music),
                Button(self.system.sound, self.system.window, f"UI SFX:", center_x, self.system.window.get_height() // 2 + spacing * 2, 240, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.toggle_ui_sfx),
                Button(self.system.sound, self.system.window, f"Game SFX:", center_x, self.system.window.get_height() // 2 + spacing * 3, 340, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.toggle_game_sfx),
                Button(self.system.sound, self.system.window, "Back", center_x, self.system.window.get_height() // 2 + spacing * 4, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings)
            ]
        elif self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Yes", center_x - btn_width, self.system.window.get_height() // 2 + spacing * 0.4, 90, btn_height, (255, 255, 255), self.button_action_true_color, self.leaderboard_opt_in_dev),
                    Button(self.system.sound, self.system.window, f"No", center_x + btn_width, self.system.window.get_height() // 2 + spacing * 0.4, 80, btn_height, (255, 255, 255), self.button_action_true_color, self.leaderboard_opt_out),
                ]
            else:
                self.buttons = [
                    Button(self.system.sound, self.system.window, f"Yes", center_x - btn_width, self.system.window.get_height() // 2 + spacing * 0.4, 90, btn_height, (255, 255, 255), self.button_action_true_color, self.leaderboard_opt_in),
                    Button(self.system.sound, self.system.window, f"No", center_x + btn_width, self.system.window.get_height() // 2 + spacing * 0.4, 80, btn_height, (255, 255, 255), self.button_action_true_color, self.leaderboard_opt_out),
                ]
        elif self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.buttons = [
                Button(self.system.sound, self.system.window, f"Submit", center_x, self.system.window.get_height() // 2 + spacing * 1.4, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.submit_username),
                Button(self.system.sound, self.system.window, f"Back", center_x, self.system.window.get_height() // 2 + spacing * 2.4, btn_width, btn_height, (255, 255, 255), self.button_action_true_color, self.back_to_root),
            ]
    
        elif self.state.is_state(MENUSTATE.LEADERBOARDVIEWER):
            self.buttons = [
                Button(self.system.sound, self.system.window, "Back", window_w - window_w // 8, window_h - 100, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.leaderboard_back_to_root),
            ]
        elif self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.buttons = [
                Button(self.system.sound, self.system.window, "Reset Username", center_x, self.system.window.get_height() // 2 - spacing, btn_width + 50, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.reset_username),
                Button(self.system.sound, self.system.window, "Change Leaderboard Opt-in Status", center_x, self.system.window.get_height() // 2, btn_width * 2 + 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.change_opt_in),
                Button(self.system.sound, self.system.window, "Back", center_x, self.system.window.get_height() // 2 + spacing, 150, btn_height,
                    (255, 255, 255), self.button_action_true_color, self.go_to_settings),
            ]

    def endless(self):
        self.system.initialize_application(GAME_MODE.ENDLESS)

    def blitz(self):
        pass
    
    def tutorial(self):
        self.system.initialize_application(GAME_MODE.TUTORIAL)

    def back_to_root_changelog(self):
        if self.system.control_state.is_state(DEVELOPER_MODE.ON):
            self.system.save.write_envar('recentlyupdated', 'true')
        else:
            self.system.save.write_envar('recentlyupdated', 'false')
        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def open_website(self):
        webbrowser.open("https://snowblitz.net", new=2)

    def discord_invite(self):
        webbrowser.open("https://discord.gg/PaWjydfUFX", new=2)


    def developer_settings(self):
        self.state.set_state(MENUSTATE.DEVELOPERSETTINGS)
        self.create_buttons()
    
    def change_opt_in(self):
        self.state.set_state(MENUSTATE.LEADERBOARDOPTIN)
        self.create_buttons()

    def reset_username(self):
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()

    def submit_username(self):
        success = self.user_creator.submit()

        if not success:
            self.set_query(self.user_creator.error)
            return

        self.state.set_state(MENUSTATE.ROOT)
        self.create_buttons()

    def leaderboard_back_to_root(self):
        self.leaderboard.fetch_manager.set_state(FETCH_STATE.CANCELLED)
        self.back_to_root()

    def leaderboard_opt_in(self):
        self.system.save.write_constant('leaderboard_opt_in','YES')
        self.query = None
        self.state.set_state(MENUSTATE.CREATEUSERNAME)
        self.create_buttons()
    
    def leaderboard_opt_in_dev(self):
        if self.system.load.read_constant('username') == None:
            self.system.save.write_constant('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.CREATEUSERNAME)
            self.create_buttons()
        else:
            self.system.save.write_constant('leaderboard_opt_in','YES')
            self.query = None
            self.state.set_state(MENUSTATE.ROOT)
            self.create_buttons()

    
    def leaderboard_opt_out(self):
        self.system.save.write_constant('leaderboard_opt_in', 'NO')
        self.state.set_state(MENUSTATE.ROOT)
        self.system.save.write_constant("username","Player")
        self.system.save.write_constant("high_score",0)
        
        self.create_buttons()
        self.query = None
        
    def view_leaderboard(self):
        self.state.set_state(MENUSTATE.LEADERBOARDVIEWER)
        self.leaderboard.refresh()
        self.create_buttons()

    def credits_callback(self):
        self.state.set_state(MENUSTATE.CREDITS)
        self.create_buttons()

    def audio_settings(self):
        self.state.set_state(MENUSTATE.AUDIO)
        self.create_buttons()

    def back_to_root(self):
        self.state.set_state(MENUSTATE.ROOT)
        self.set_query("")
        self.create_buttons()
    
    def go_to_settings(self):
        self.state.set_state(MENUSTATE.SETTINGS)
        self.create_buttons()

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == self.system.input.video_resize_event():
            self.scale()
        self.user_creator.handle_event(event)
        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            keys = self.system.input.get_pressed_keys()
            if keys[self.system.input.keys.return_key()]:
                self.submit_username()

    def scale(self):
        self.rescale_assets()
        self.create_buttons()

    def draw(self):
        if self.system.sound.current_track is None and self.system.sound.music_state.is_state(MUSIC_STATE.ON):
            self.system.sound.play_music()
        
        t = self.system.time.get_current_time() / 1000
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)

        if self.state.is_state(MENUSTATE.LEADERBOARDOPTIN):
            self.set_title(None)
            self.set_query("DO YOU AGREE TO HAVE YOUR SCORES POSTED ON A GLOBAL LEADERBOARD?")

        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.draw(mouse_pos)

        if self.state.is_state(MENUSTATE.CREATEUSERNAME):
            self.set_title(None)
            self.set_query(self.user_creator.error if self.user_creator.error else "Please enter a username:")
            self.user_creator.draw()

        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.CURRENT):
            self.set_title("")
            self.draw_username_text(f"{self.system.user.username}")
            if self.system.user.high_score is not None:
                self.draw_score_text(f"{self.system.user.high_score}")
            else:
                self.draw_score_text(f"{self.system.load.read_constant('high_score')}")
            self.system.window.blit(self.title_image, self.title_rect)
        
        if self.state.is_state(MENUSTATE.ROOT) and self.updater.state.is_state(UPDATE_STATE.AVAILABLE):
            self.set_title("")
            self.draw_update_text()
            self.draw_username_text(f"{self.system.load.read_constant('username')}")
            self.draw_score_text(f"{self.system.load.read_constant('high_score')}")
            self.system.window.blit(self.title_image, self.title_rect)

        if self.state.is_state(MENUSTATE.SETTINGS):
            self.set_title("SETTINGS")
        
        if self.state.is_state(MENUSTATE.DEVELOPERSETTINGS):
            self.set_title('DEVELOPER SETTINGS')

        if self.state.is_state(MENUSTATE.CREDITS):
            self.set_title("CREDITS:")
            self.credits.draw()

        if self.state.is_state(MENUSTATE.CHANGELOG):
            self.set_title("CHANGELOG:")
            self.change_log.draw()

        if self.state.is_state(MENUSTATE.AUDIO):
            self.set_title("AUDIO SETTINGS")
        
        if self.state.is_state(MENUSTATE.LEADERBOARDVIEWER):
            self.leaderboard.fetch_and_display()
            self.set_title("Top 10 Leaderboard")

        self.draw_title()