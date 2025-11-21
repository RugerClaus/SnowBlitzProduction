import os
import pygame
import json
from datetime import datetime

def asset(asset):
    if asset == "title":
        return "assets/images/main/title.png"
    elif asset == "default_font":
        return 'assets/font/Pixeltype.ttf'
    elif asset == "background":
        return "assets/images/raycasted/stars.png"
    elif asset == "gunnoshot":
        return "assets/images/raycasted/gunnoshot.png"
    
def asset_frames(prefix, count, ext="png", folder="menu_bg"):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join("assets", "images", "main",folder, f"{prefix}_{i}.{ext}")
        surf = pygame.image.load(path).convert_alpha()
        frames.append(surf)
    return frames

def log_state_transition(from_state, to_state, state_type, log_file=None):
    import os
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "from": str(from_state),
        "to": str(to_state)
    }

    if not log_file:
        log_dir = f"logs/{state_type}_Logs"
        os.makedirs(log_dir, exist_ok=True)   # Create folder if missing
        log_file = os.path.join(log_dir, f"{state_type.lower()}_transitions.log")

    with open(log_file, "a") as f:
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
    type = type.lower()
    if type == "music":
        return f"assets/sounds/music"
    elif type == "sfx":
        return f"assets/sounds/sfx"
    else:
        print("Can't find audio path!")
        return None