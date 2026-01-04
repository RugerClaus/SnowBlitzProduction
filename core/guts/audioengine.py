import pygame
import random
import os
from mutagen import File
from helper import audio_path,log_error

class AudioEngine:
    def __init__(self):
        self.initialize_audio()
        

        self.music_tracks = {}
        self.sound_effects = {}
        self.active_sfx = {}
        self.volume = 0.5
        self.music_active = True
        self.music_queue = []
        self.current_track = None

        self.load_audio_files()

    def initialize_audio(self):
        try:
            pygame.mixer.init()
            self.MUSIC_END_EVENT = pygame.USEREVENT + 1
            pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)
            print("Audio device initialized successfully.")
            
        except pygame.error:
            
            log_error(f"No available audio device. Retrying... PyGame: {str(pygame.error)}")

    def load_audio_files(self):
        self.load_music_tracks()
        self.load_sound_effects()
    
    def load_music_tracks(self):
        music_dir = audio_path("music")
        for filename in os.listdir(music_dir):
            if filename.endswith(('.mp3', '.ogg', '.wav')):
                track_path = os.path.join(music_dir, filename)
                audio_file = File(track_path)
                title = audio_file.get('title', [filename])[0]
                self.music_tracks[title] = track_path
            self.music_queue = list(self.music_tracks.keys())
            random.shuffle(self.music_queue)
    
    def load_sound_effects(self):
        sfx_dir = audio_path("sfx")
        for filename in os.listdir(sfx_dir):
            if filename.endswith(('.mp3', '.ogg', '.wav')):
                sfx_path = os.path.join(sfx_dir, filename)
                sound_file = File(sfx_path)
                effect_name = sound_file.get('title', [filename])[0]
                effect_name = os.path.splitext(effect_name)[0]
                self.sound_effects[effect_name] = os.path.join(sfx_dir, filename)
    
    def play_sfx(self, effect_name):
        if effect_name in self.sound_effects:
            sfx_path = self.sound_effects[effect_name]
            sound_effect = pygame.mixer.Sound(sfx_path)
            sound_effect.set_volume(self.volume)
            sound_effect.play()
            self.active_sfx[effect_name] = sound_effect
        else:
            print(f"Sound effect '{effect_name}' not found.")
    
    def stop_sfx(self, effect_name):
        if effect_name in self.active_sfx:
            self.active_sfx[effect_name].stop()
            del self.active_sfx[effect_name]

    def stop_all_sfx(self):
        print('Stopping all SFX')
        for sfx in self.active_sfx.values():
            sfx.stop()
        self.active_sfx.clear()

    def play_music(self, mode="random"):
        if mode == "random":
            self.music_active = True
            if not self.music_queue:
                self.music_queue = list(self.music_tracks.keys())
                random.shuffle(self.music_queue)

            # Play the next track in the queue
            next_track = self.music_queue.pop()
            self.current_track = next_track
            pygame.mixer.music.load(self.music_tracks[next_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

        elif mode == "loop":
            self.music_active = True
            if self.current_track is None:
                return
            pygame.mixer.music.load(self.music_tracks[self.current_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

        elif mode == "stop":
            self.music_active = False
            self.current_track = None
            pygame.mixer.music.stop()

        elif isinstance(mode, str):
            if mode in self.music_tracks:
                pygame.mixer.music.load(self.music_tracks[mode])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()

        else:
            raise ValueError("Invalid mode for play_music")

    def handle_music_event(self, event):
        if event.type == self.MUSIC_END_EVENT:
            if self.music_active and self.music_queue:
                self.play_music("random")

    def toggle_music(self):
        if self.music_active:
            self.play_music("stop")
            self.music_active = False
        else:
            self.play_music("random")
            self.music_active = True

    def volume_up(self):
        if self.volume < 1.0:
            self.volume += 0.1
            pygame.mixer.music.set_volume(self.volume)
    
    def volume_down(self):
        if self.volume > 0:
            self.volume -= 0.1
            pygame.mixer.music.set_volume(self.volume)