import os
import sys
import zipfile
import subprocess
from helper import log_event, log_error

# Use the folder next to the EXE if frozen
if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

GAME_EXECUTABLE = "snowblitz"

UPDATE_FOLDER = os.path.join(ROOT_DIR, "update")
UPDATE_ZIP = os.path.join(UPDATE_FOLDER, "update.zip")


def unpack_update():
    if not os.path.exists(UPDATE_ZIP):
        log_error(f"No update ZIP found at {UPDATE_ZIP}")
        sys.exit(1)

    log_event("Unpacking update...")
    try:
        with zipfile.ZipFile(UPDATE_ZIP, "r") as zip_ref:
            zip_ref.extractall(ROOT_DIR)
        log_event("Update unpacked successfully!")
    except Exception as e:
        log_error(f"Failed to unpack update: {e}")
        sys.exit(1)


def launch_game():
    exe_path = os.path.join(ROOT_DIR, GAME_EXECUTABLE)
    if os.path.exists(exe_path):
        log_event(f"Launching {GAME_EXECUTABLE}...")
        try:
            if sys.platform.startswith("win"):
                os.startfile(exe_path)
            else:
                os.chmod(exe_path, 0o755)
                subprocess.Popen([exe_path])
            log_event(f"{GAME_EXECUTABLE} launched successfully!")
        except Exception as e:
            log_error(f"Failed to launch {GAME_EXECUTABLE}: {e}")
    else:
        log_error(f"Executable not found: {exe_path}")


def main():
    unpack_update()
    launch_game()
    log_event("Updater finished successfully.")


if __name__ == "__main__":
    main()
