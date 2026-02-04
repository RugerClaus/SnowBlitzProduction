import pygame
import random
import os
from mutagen import File
from helper import *

from core.state.ApplicationLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.ApplicationLayer.Audio.Interface.statemanager import InterfaceSFXStateManager
from core.state.ApplicationLayer.Audio.Music.state import MUSIC_STATE
from core.state.ApplicationLayer.Audio.Music.statemanager import MusicStateManager
from core.state.ApplicationLayer.Audio.Game.state import GAME_SFX_STATE
from core.state.ApplicationLayer.Audio.Game.statemanager import GameSFXStateManager
from core.state.ApplicationLayer.Audio.SFX.state import SYSTEM_SFX_STATE
from core.state.ApplicationLayer.Audio.SFX.statemanager import SystemSFXStateManager

class AudioEngine:
    def __init__(self):
        default_volume = 0.3
        create_volume_files(str(default_volume))
        self.interface_sfx_state = InterfaceSFXStateManager()
        self.music_state = MusicStateManager()
        self.game_sfx_state = GameSFXStateManager()
        self.system_sfx_state = SystemSFXStateManager()
        sound_on = self.initialize_audio()
        if sound_on:
            self.interface_sfx_state.set_state(INTERFACE_SFX_STATE.ON)
            self.music_state.set_state(MUSIC_STATE.ON)
            self.game_sfx_state.set_state(GAME_SFX_STATE.ON)
            self.system_sfx_state.set_state(SYSTEM_SFX_STATE.ON)

        self.music_tracks = {}
        self.sound_effects = {}
        self.active_sfx = {}
        self.volume = float(read_constant_from_file('music_volume'))
        self.sfx_volume = float(read_constant_from_file('sfx_volume'))
        self.music_queue = []
        self.current_track = None

        self.load_audio_files()

    def initialize_audio(self):
        try:
            pygame.mixer.init()
            self.MUSIC_END_EVENT = pygame.USEREVENT + 1
            pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)
            log_event("Audio device initialized successfully.")
            return True
            
            
        except pygame.error:
            self.interface_sfx_state.set_state(INTERFACE_SFX_STATE.NONE)
            log_error(f"No available audio device. Retrying... PyGame: {str(pygame.error)}")
            return False

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
                self.sound_effects[effect_name] = pygame.mixer.Sound(sfx_path)
    
    def play_sfx(self, effect_name):
        if self.game_sfx_state.is_state(GAME_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sound_effect = self.sound_effects[effect_name]
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.game_sfx_state.is_state(GAME_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
    
        else:
            return "off"
    
    def play_ui_sfx(self, effect_name):
        if self.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sfx_path = self.sound_effects[effect_name]
                sound_effect = pygame.mixer.Sound(sfx_path)
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.game_sfx_state.is_state(INTERFACE_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
    
        else:
            return "off"
        
    def play_system_sfx(self, effect_name):
        if self.interface_sfx_state.is_state(SYSTEM_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sfx_path = self.sound_effects[effect_name]
                sound_effect = pygame.mixer.Sound(sfx_path)
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.game_sfx_state.is_state(SYSTEM_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
    
        else:
            return "off"

    def stop_sfx(self, effect_name):
        if effect_name in self.active_sfx:
            self.active_sfx[effect_name].stop()
            del self.active_sfx[effect_name]

    def stop_all_sfx(self):
        log_event('Stopping all SFX')
        for sfx in self.active_sfx.values():
            sfx.stop()
        self.active_sfx.clear()

    def play_music(self, mode="random"):
        if mode == "random":
            self.music_state.set_state(MUSIC_STATE.ON)
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
            self.music_state.set_state(MUSIC_STATE.ON)
            if self.current_track is None:
                return
            pygame.mixer.music.load(self.music_tracks[self.current_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

        elif mode == "stop":
            self.music_state.set_state(MUSIC_STATE.OFF)
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
            if self.music_state.is_state(MUSIC_STATE.ON) and self.music_queue:
                self.play_music("random")

    def toggle_music(self):
        if self.music_state.is_state(MUSIC_STATE.ON):
            self.play_music("stop")
            self.music_state.is_state(MUSIC_STATE.OFF)
        else:
            self.play_music("random")
            self.music_state.set_state(MUSIC_STATE.ON)

    def volume_up(self):
        if self.volume < 0.5:
            self.volume += 0.1
            self.volume = round(self.volume, 1)
            write_constant_to_file('music_volume',str(self.volume))
            pygame.mixer.music.set_volume(self.volume)
    
    def volume_down(self):
        if self.volume > 0:
            self.volume -= 0.1
            self.volume = round(self.volume, 1)
            write_constant_to_file('music_volume',str(self.volume))
            pygame.mixer.music.set_volume(self.volume)

    def sfx_volume_up(self):
        if self.sfx_volume < 0.5:
            self.sfx_volume += 0.1
            self.sfx_volume = round(self.sfx_volume, 1)
            write_constant_to_file('sfx_volume',str(self.sfx_volume))
    
    def sfx_volume_down(self):
        if self.sfx_volume > 0:
            self.sfx_volume -= 0.1
            self.sfx_volume = round(self.sfx_volume, 1)
            write_constant_to_file('sfx_volume',str(self.sfx_volume))