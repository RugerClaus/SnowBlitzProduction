import pygame
from core.guts.input.iostream import IOSTREAM
from core.ui.font import FontEngine


class InputManager:
    def __init__(self, window):
        self.iostream = IOSTREAM()
        self.current_keys = set()
        self.released_keys = set()
        self.key_history = {}
        self.surface = window.make_surface(window.get_width(), window.get_height(), True)
        self.font = FontEngine("keypress").font
        self.window = window
        self.last_key = None
        self.last_key_time = 0
        self.key_display_timeout = 1000

    def handle_event(self, event,gameplay=False):
        now = pygame.time.get_ticks()
        if gameplay:
            if event.type == pygame.KEYDOWN:
                self.current_keys.add(event.key)
                self.key_history[event.key] = now
                self.last_key = event.key
                self.last_key_time = now

                return event.key
        
        else:
            if event.type == pygame.KEYDOWN:
                self.current_keys.add(event.key)
                self.key_history[event.key] = now
                self.last_key = event.key
                self.last_key_time = now

                command = self.iostream.update(event)
                return command

            elif event.type == pygame.KEYUP:
                self.current_keys.discard(event.key)
                self.released_keys.add(event.key)

            return None
        
    def rescale(self,w,h):
        self.surface = self.window.make_surface(w,h,True)
        self.draw_most_recent_keypress()


    def draw_most_recent_keypress(self):
        self.surface.fill((0, 0, 0, 0))  
        now = pygame.time.get_ticks()

        self.key_history = {k: t for k, t in self.key_history.items() if now - t < self.key_display_timeout}

        recent_keys = list(self.key_history.keys())

        if recent_keys:
            key_names = [pygame.key.name(key) for key in recent_keys]
            keys_str = ", ".join(key_names)
            letter = self.font.render(keys_str, False, (255, 255, 255))
            rect = letter.get_rect(center=(self.surface.get_width() // 2,
                                           letter.get_rect().height))
            self.surface.blit(letter, rect)
        else:
            self.last_key = None

        self.window.blit(self.surface, (0, 0))

    def is_pressed(self, key):
        return key in self.current_keys

    def was_released(self, key):
        return key in self.released_keys

    def clear_released(self):
        self.released_keys.clear()