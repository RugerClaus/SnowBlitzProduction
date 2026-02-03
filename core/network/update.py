import os
import requests
from helper import log_error, log_event
from config import config
from core.state.ApplicationLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.ApplicationLayer.NetworkLayer.Loading.statemanager import FetchStateManager
from core.state.ApplicationLayer.NetworkLayer.Update.state import UPDATE_STATE
from core.state.ApplicationLayer.NetworkLayer.Update.statemanager import UpdateStateManager
from enum import Enum

TIMEOUT_SECONDS = 5

class Update:
    def __init__(self):
        self.currentVersionURL = 'https://snowblitz.net/api/getCurrentGameVersion.php'
        self.state = UpdateStateManager()
        self.fetch_state_manager = FetchStateManager()

        self.fetch_current_version_data()
        self.update_folder = "update"

    def fetch_current_version_data(self):
        try:
            response = requests.get(self.currentVersionURL, timeout=TIMEOUT_SECONDS)

            if response.status_code == 200:
                version_data = response.json()
                log_event(f"Fetched version data. Status: {response.status_code}; Response: {version_data}")

                # Extract version number from the 'data' list
                data = version_data.get("data", [])
                if data:
                    self.server_version = data[0].get("version_number")
                else:
                    self.server_version = None

                current_version = config.get("VERSION")

                if self.server_version is None:
                    log_error(f"Version number missing in server response: {version_data}")
                    return ("error", "Version number missing in server response.")

                log_event(f"Server version: {self.server_version}, Current version: {current_version}")

                if self.server_version == current_version:
                    self.state.set_state(UPDATE_STATE.CURRENT)
                    log_event("App is up to date.")
                    return ("success", "App is up to date.")
                
                elif self.server_version > current_version:
                    self.state.set_state(UPDATE_STATE.AVAILABLE)
                    log_event("Update available!")
                    return ("success", "Update available!")
                
                else:
                    self.state.set_state(UPDATE_STATE.CURRENT)
                    log_event("You are up-to-date. No updates available.")
                    return ("success", "You are up-to-date.")

            else:
                log_error(f"Failed to fetch version data. Status: {response.status_code}; Response: {response.text}")
                return ("error", f"HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            log_error("Version data fetch timed out.")
            return ("timeout", "Failed to fetch version data: Timeout")

        except requests.exceptions.RequestException as e:
            log_error(f"Network error while fetching version data: {e}")
            return ("error", str(e))

    def start(self):
        log_event(f"Starting the update process... from {config.get('VERSION')} to {self.server_version}")

        os_type = config.get("OS").lower()
        update_files_url = f'https://snowblitz.net/downloads/update/latest/{os_type}'

        log_event(f"Download URL: {update_files_url}")

        if not self.download_update_files(update_files_url):
            log_error("Failed to download update files.")
            return ("error", "Failed to download update files.")

    def download_update_files(self, update_files_url):
        self.fetch_state_manager.set_state(FETCH_STATE.FETCHING)

        try:
            response = requests.get(update_files_url, timeout=TIMEOUT_SECONDS)

            if response.status_code == 200:
                files_data = response.json()
                log_event(f"Fetched update files. Status: {response.status_code}; Response: {files_data}")

                files_to_download = files_data.get('files', [])

                if not files_to_download:
                    log_error("No update files found.")
                    self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
                    return False

                os_type = config["OS"].lower()

                files_for_os = []
                for file_info in files_to_download:
                    if os_type in file_info['name'].lower():
                        files_for_os.append(file_info)

                if not files_for_os:
                    log_error(f"No update files found for OS: {os_type}")
                    self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
                    return False

                total_files = len(files_for_os)
                downloaded_files = 0

                # Download files and update progress
                for file_info in files_for_os:
                    file_url = file_info['url']
                    file_name = file_info['name']
                    file_path = self.download_file(file_url, file_name)

                    if file_path:
                        downloaded_files += 1
                        self.fetch_state_manager.update_progress(int((downloaded_files / total_files) * 100))

                log_event("All update files downloaded successfully.")
                self.fetch_state_manager.set_state(FETCH_STATE.SUCCESS)
                return True

            else:
                log_error(f"Failed to fetch update files. Status: {response.status_code}; Response: {response.text}")
                self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
                return False

        except requests.exceptions.Timeout:
            log_error("Timeout occurred while fetching update files.")
            self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
            return False

        except requests.exceptions.RequestException as e:
            log_error(f"Network error while fetching update files: {e}")
            self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
            return False

    def download_file(self, file_url, file_name):
        try:
            response = requests.get(file_url, timeout=TIMEOUT_SECONDS, stream=True)

            if response.status_code == 200:
                file_path = os.path.join(self.update_folder, file_name)

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                log_event(f"Downloaded {file_name} successfully to {file_path}")
                return file_path
            else:
                log_error(f"Failed to download {file_name}. HTTP status code: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            log_error(f"Timeout occurred while downloading {file_name}.")
            return None
        except requests.exceptions.RequestException as e:
            log_error(f"Network error while downloading {file_name}: {e}")
            return None
