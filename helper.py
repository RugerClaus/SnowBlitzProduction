import os
import pygame
import json
from datetime import datetime

def asset(asset):
    if asset == "title":
        return "assets/images/main/title.png"
    elif asset == "default_font":
        return 'assets/font/Pixeltype.ttf'
    
def asset_frames(prefix, count, ext="png", folder="menu_bg"):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join("assets", "images", "main",folder, f"{prefix}_{i}.{ext}")
        surf = pygame.image.load(path).convert_alpha()
        frames.append(surf)
    return frames

def log_system_state_transitions(from_state,to_state,state_type):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "from": str(from_state),
        "to": str(to_state)
    }
    with open("logs/Main_State_Logs/app_state_transitions.log", "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_entity_state_transitions(from_state,to_state,state_type):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "from": str(from_state),
        "to": str(to_state)
    }
    with open("logs/Entities_State_Logs/entity_state_transitions.log", "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_app_mode_transitions(from_mode,to_mode):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": "APPMODE",
        "from": str(from_mode),
        "to": str(to_mode)
    }
    with open("logs/Mode_Logs/mode_transitions.log", "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_scene_transitions(from_scene,to_scene,SCENETYPE):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": str(SCENETYPE),
        "from": str(from_scene),
        "to": str(to_scene)
    }
    with open("logs/Scenes/all_scene_transitions.log", "a") as f:
        f.write(json.dumps(log_data) + "\n")

def get_colors(color):
    if color == "red":
        return (255,0,0)
    elif color  == "green":
        return (0,255,0)
    elif color == "blue":
        return (0,0,255)
    elif color == "purple":
        return (128,0,128)
    elif color == "black":
        return (0,0,0)
    elif color == "white":
        return (255,255,255)
    else:
        print("Can't find color!")
        return (128,128,128)
    
def audio_path(type):
    type.lower()
    if type == "music":
        return f"assets/sounds/music"
    elif type == "sfx":
        return f"assets/sounds/sfx"