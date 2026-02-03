import os
import sys
import zipfile
import shutil
import subprocess
from helper import log_event, log_error

if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

GAME_EXECUTABLE = "snowblitz"
UPDATE_ZIP = os.path.join(ROOT_DIR, "update.zip")


def unpack_update():
    if not os.path.exists(UPDATE_ZIP):
        log_error(f"No update ZIP found at {UPDATE_ZIP}")
        sys.exit(1)

    log_event(f"Unpacking update from {UPDATE_ZIP}...")
    try:
        with zipfile.ZipFile(UPDATE_ZIP, "r") as zip_ref:
            zip_ref.extractall(ROOT_DIR)

        extracted_folders = [
            name for name in os.listdir(ROOT_DIR)
            if os.path.isdir(os.path.join(ROOT_DIR, name)) and name.startswith("snowblitz_update")
        ]

        if not extracted_folders:
            log_error("No extracted update folder found after unpacking")
            sys.exit(1)

        extracted_folder = os.path.join(ROOT_DIR, extracted_folders[0])
        log_event(f"Moving files from {extracted_folder} into root directory...")

        for item in os.listdir(extracted_folder):
            src = os.path.join(extracted_folder, item)
            dst = os.path.join(ROOT_DIR, item)

            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)

            shutil.move(src, dst)

        os.rmdir(extracted_folder)
        log_event("Update unpacked and merged successfully!")

    except zipfile.BadZipFile:
        log_error(f"Failed to unpack update: bad ZIP file {UPDATE_ZIP}")
        sys.exit(1)
    except Exception as e:
        log_error(f"Failed to unpack update: {e}")
        sys.exit(1)


def launch_game():
    exe_path = os.path.join(ROOT_DIR, GAME_EXECUTABLE)
    if not os.path.exists(exe_path):
        log_error(f"Executable not found: {exe_path}")
        return

    log_event(f"Launching {GAME_EXECUTABLE} at {exe_path}...")
    try:
        if sys.platform.startswith("win"):
            os.startfile(exe_path)
        else:
            os.chmod(exe_path, 0o755)
            subprocess.Popen([exe_path])
        log_event(f"{GAME_EXECUTABLE} launched successfully!")
    except Exception as e:
        log_error(f"Failed to launch {GAME_EXECUTABLE}: {e}")


def main():
    log_event("Updater started.")
    unpack_update()
    launch_game()
    log_event("Updater finished successfully.")


if __name__ == "__main__":
    main()
