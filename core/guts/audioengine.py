import pygame
import random
import os
from mutagen import File
from helper import audio_path

class AudioEngine:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)

        self.music_tracks = {}
        self.sound_effects = {}
        self.volume = volume
        self.music_active = True
        self.sfx_active = True
        self.music_queue = []
        self.current_track = None

        self.load_audio_files()

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
    
    def play_music(self, mode="random"):
        if mode == "random":
            if not self.music_queue:
                self.music_queue = list(self.music_tracks.keys())
                random.shuffle(self.music_queue)

            next_track = self.music_queue.pop()
            self.current_track = next_track
            pygame.mixer.music.load(self.music_tracks[next_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
        
        elif mode == "loop":
            if self.current_track is None:
                return
            pygame.mixer.music.load(self.music_tracks[self.current_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

        elif mode == "stop":
            self.current_track = None
            pygame.mixer.music.stop()

        elif isinstance(mode, str):
            # Assume it's a track title
            if mode in self.music_tracks:
                pygame.mixer.music.load(self.music_tracks[mode])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()

        else:
            raise ValueError("Invalid mode for play_music")
