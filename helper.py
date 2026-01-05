import os
import pygame
import json
from datetime import datetime

def asset(asset):
    if asset == "title":
        return "assets/images/main/title.png"
    elif asset == "default_font":
        return 'assets/font/Pixeltype.ttf'
    elif asset == "splash":
        return "assets/images/main/splash.png"
    elif asset == "gunnoshot":
        return "assets/images/raycasted/gunnoshot.png"
    elif asset == "gunshot":
        return "assets/images/raycasted/gunshot.png"
    
def asset_frames(prefix, count, ext="png", folder="menu_bg"):
    frames = []
    for i in range(1, count + 1):
        path = os.path.join("assets", "images", "main",folder, f"{prefix}_{i}.{ext}")
        surf = pygame.image.load(path).convert_alpha()
        frames.append(surf)
    return frames

def log_state_transition(from_state, to_state, state_type, sub_dir=None, log_file=None):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "from": str(from_state),
        "to": str(to_state)
    }
    if sub_dir:
        log_dir = f"logs/{sub_dir}/{state_type}_Logs"
    else:
        log_dir = f"logs/{state_type}_Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{state_type.lower()}_transitions.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_error(error,object=None):
    log_file = f"logs/error.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "error": f"What happened: {error}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_event(event,object=None):
    log_file = f"logs/event.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event": f"What happened: {event}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
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
    
import os

def write_constant_to_file(filename, value):
    constants_dir = 'saves/constants'
    
    if not os.path.exists(constants_dir):
        os.makedirs(constants_dir)

    file_path = os.path.join(constants_dir, filename)
    
    try:
        with open(file_path, 'w') as file:
            file.write(str(value))
        log_event(f"Constant '{value}' written to {file_path}")
    except Exception as e:
        log_event(f"Error writing to file: {e}")

def read_constant_from_file(filename):
    file_path = os.path.join('saves/constants', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            log_event(f"File {file_path} does not exist.")
            return None
    except Exception as e:
        log_error(f"Error reading from file: {e}")
        return None

def check_leaderboard_opt():
    opt_in = read_constant_from_file('leaderboard_opt_in')
    if opt_in is not None:
        return True
    else:
        return False