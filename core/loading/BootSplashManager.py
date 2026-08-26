from helper import asset
from core.state.RuntimeLayer.BootSplash.state import BOOT_SPLASH_STATE
from core.state.RuntimeLayer.BootSplash.statemanager import BootSplashStateManager
from core.application.SnowBlitz.entities.entitymanager import EntityManager

from core.ui.widgets.image import Image


class BootSplashManager:

    MAX_SPLASHES = 5

    def __init__(self, system):

        self.system = system
        self.state = BootSplashStateManager()
        self.entitymanager = EntityManager(self.system)

        self.splashes = []

        self.current_splash = 0
        self.splash_start_time = self.system.time.get_current_time()

        self.sfx_played = []

        for i in range(1, self.MAX_SPLASHES + 1):

            image_name = f"splashpt{i}"
            sfx_name = f"splash{i}"

            splash_asset = asset(image_name)

            if splash_asset and splash_asset.exists():

                image = Image(
                    self.system,
                    f"splash_{i}",
                    image_name,
                    position=(0.5, 0.5),
                    scale=0.75
                )

                duration = self.system.sound.get_sfx_length(sfx_name)

                if duration == 0:
                    duration = 3000

                self.splashes.append({
                    "image": image,
                    "sfx": sfx_name,
                    "duration": duration
                })

                self.sfx_played.append(False)


        self.state.set_state(BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE)


    def handle_event(self, event, command=None):

        keys = self.system.input.keys

        if event.type == self.system.input.keydown():

            if (
                event.key == keys.space_key()
                or event.key == keys.return_key()
                or event.key == keys.escape_key()
            ):
                self.system.sound.stop_all_sfx()
                self.state.set_state(BOOT_SPLASH_STATE.NONE)


        if event.type == self.system.input.mouse_button_down() and event.button == 1:

            self.next_splash()


    def next_splash(self):

        self.system.sound.stop_all_sfx()

        self.current_splash += 1
        self.splash_start_time = self.system.time.get_current_time()

        if self.current_splash >= len(self.splashes):

            self.system.clean_up_states([self.state.state])
            self.state.set_state(BOOT_SPLASH_STATE.NONE)
            return

        states = [
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_ONE,
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_TWO,
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_THREE,
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FOUR,
            BOOT_SPLASH_STATE.BOOT_SPLASH_SCREEN_FIVE,
        ]

        self.state.set_state(states[self.current_splash])


    def scale(self):

        for splash in self.splashes:
            splash["image"].scale()


    def update(self):

        if self.state.is_state(BOOT_SPLASH_STATE.NONE):
            self.system.initialize_application()
            return


        if self.current_splash == 2:

            self.entitymanager.update_entities()
            self.entitymanager.spawn_snowflakes()
            self.entitymanager.spawn_powerups(20)
            self.entitymanager.spawn_rocks(20)


    def play_current_splash(self):

        if self.current_splash >= len(self.splashes):

            self.state.set_state(BOOT_SPLASH_STATE.NONE)
            return


        current_time = self.system.time.get_current_time()

        splash = self.splashes[self.current_splash]

        image = splash["image"]
        sfx = splash["sfx"]
        duration = splash["duration"]


        if not self.sfx_played[self.current_splash]:

            self.system.sound.play_sfx(sfx)
            self.sfx_played[self.current_splash] = True


        elapsed = current_time - self.splash_start_time

        alpha = min((elapsed / max(1, duration)) * 255, 255)
        if self.current_splash == 2:
            image.set_alpha(alpha)
        image.draw()


        if elapsed >= duration:

            self.next_splash()


    def draw(self):

        if self.state.is_state(BOOT_SPLASH_STATE.NONE):
            return


        self.play_current_splash()

        if self.current_splash == 2:
            self.entitymanager.draw_entities()