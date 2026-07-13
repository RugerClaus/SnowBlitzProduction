from core.ui.newbutton import Button
from core.menus.basemenu import BaseMenu

class Win(BaseMenu):
    def __init__(self, system, restart_callback):
        self.system = system
        super().__init__(system)
        self.restart_callback = restart_callback
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        
        self.buttons = [
            Button(
                self.system,
                50,
                "Restart",
                (0.5,0.4),
                self.restart_callback
            ),
            Button(
                self.system,
                50,
                "Main Menu",
                (0.5,0.5),
                self.system.go_to_menu
            ),
            Button(
                self.system,
                50,
                "Quit",
                (0.5,0.6),
                self.system.quit
            )
        ]

    def on_resize(self):
        self.create_buttons()

    def handle_event(self, event):
        if event.type == self.system.input.mouse_button_down() and event.button == 1:
            mouse_pos = self.system.input.get_mouse_pos()
            for button in self.buttons:
                button.is_clicked(mouse_pos, True)
        elif event.type == self.system.input.video_resize_event():
            self.on_resize()

    def draw(self):
        t = self.system.time.get_current_time() / 1000
        pulse = (self.system.math.sin(t) + 1) / 2
        fade_color = (
            int(20 + (35 - 20) * pulse),
            0,
            int(20 + (35 - 20) * pulse)
        )
        self.system.window.fill(fade_color)

        text = self.font.render(f"YOU WIN!", True, (50, 200, 50))
        rect = text.get_rect(center=(self.system.window.get_screen().get_width() // 2, self.system.window.get_screen().get_height() // 4))
        self.system.window.blit(text, rect)

        for button in self.buttons:
            button.draw()

    def update(self):
        mouse_pos = self.system.input.get_mouse_pos()
        for button in self.buttons:
            button.update(mouse_pos)