import math
from pathlib import Path
import platform


from datetime import datetime
import json,os

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

def log_warning(warning,object=None):
    log_file = f"logs/warning.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "warning": f"What happened: {warning}"
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

def log_state_transition(from_state, to_state, state_type, ticks=None, log_file=None):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "ticks": ticks,
        "from": str(from_state),
        "to": str(to_state)
    }
    log_dir = f"logs/{state_type}_Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{state_type.lower()}_transitions.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data) + "\n")


def log_debug(error,object=None):
    log_file = f"logs/debug.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "error": f"What happened: {error}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

config = {
    "TITLE": "Snow Blitz Beta prelease 3 of",
    "VERSION": "1.0.0-beta",
    "FRAMEWORK VERSION": "0.7.1-alpha",
    "OS": platform.system(),
    "OSV": platform.version(),
    "OSR": platform.release(),
    "UPDATE_ZIP_NAME": "snowblitz_update_latest.zip",
    "UPDATER_WINDOWS": "updater.exe",
    "UPDATER_LINUX": "updater",
    "UPDATER_VERSION": "0.0.2",
    "WINDOW_BACKEND": "draw",
    "NSTATURL": "https://snowblitz.net",
    "SPLASHSCREEN": True,
    "API_KEY": "astonished-Apes-are-fuckingsillynshitKi11urself,bitch yeah",
    "API": {
        "LEADERBOARD": "https://snowblitz.net/api/sbGetLeaderboard.php",
        "REGISTRATION_URL": "https://snowblitz.net/api/createNewUser.php",
        "LOGIN_URL": "https://snowblitz.net/api/loginClient.php",
        "UPDATE_SCORE": "https://snowblitz.net/api/sbLeaderboard.php",
        "UPDATE_FILE_URL": "https://snowblitz.net/downloads/update",
        "CURRENT_VERSION": "https://snowblitz.net/api/getCurrentUpdaterVersion.php",
        "CREATE_SESSION": "https://snowblitz.net/api/createGameSession.php",
    },
    "ASSETS": {
        "title": "assets/images/main/title.png",
        "default_font": "assets/font/OpenSansPX.ttf",
        "bold": "assets/font/OpenSansPXBold.ttf",

        "splashpt1": "assets/images/main/splashpt1.png",
        "splashpt2": "assets/images/main/splashpt2.png",
        "splashpt3": "assets/images/main/splashpt3.png",
        "splashpt4": "assets/images/main/splashpt4.png",
        "splashpt5": "assets/images/main/splashpt5.png",
        

        "splash1": "assets/sounds/sfx/splash1.ogg",
        "splash2": "assets/sounds/sfx/splash2.ogg",
        "splash3": "assets/sounds/sfx/splash3.ogg",
        "splash4": "assets/sounds/sfx/splash4.ogg",
        "splash5": "assets/sounds/sfx/splash5.ogg",

        "button_clicked": "assets/sounds/sfx/button_clicked.mp3",

        "linux_icon": "assets/images/build/linux.png",
        "windows_icon": "assets/images/build/windows.ico",

        "clock": "assets/images/main/clock.png",

        "snowflakes": "assets/images/muyuta/snowflakes.png",

        #shaders
        "v": "core/draw/shaders/v.glsl",
        "f": "core/draw/shaders/f.glsl",
        "texturev": "core/draw/shaders/texturev.glsl",
        "texturef": "core/draw/shaders/texturef.glsl",
        "cube": "core/draw/shaders/cube.glsl",
        "plane": "core/draw/shaders/plane.glsl",
        "rectpulse": "core/draw/shaders/rectpulse.glsl",
        "fcellshader": "core/draw/shaders/fcellshader.glsl"
    }

}

def sine(current_time):
    t = current_time / 1000
    pulse = (math.sin(t) + 1) / 2
    return pulse
def load_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def asset(name):
    path = config.get("ASSETS", {}).get(name)

    if path is None:
        return None

    return Path(path)
    
def audio_path(type):
    type = type.lower()
    if type == "music":
        return f"assets/sounds/music"
    elif type == "sfx":
        return f"assets/sounds/sfx"
    else:
        log_error("Can't find audio path!")
        return None