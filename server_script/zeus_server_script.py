import os
import configparser
import socket
import threading
import sys
import signal
import time
import vgamepad as vg
import random
import os
import platform
import signal
import subprocess
import requests
import zipfile
import shutil



class GamepadController:
    def __init__(self, config_path="config.ini"):
        self.running = True
        self.anti_afk_enabled = True
        self.movement_enabled = False
        self.gamepad = vg.VX360Gamepad()
        self.load_config(config_path)

    def load_config(self, config_path):
        """Load configuration from config file."""
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        # Load Anti-AFK settings
        self.anti_afk_interval = self.config.getfloat('AntiAFK', 'interval', fallback=60)
        self.right_bumper_duration = self.config.getfloat('AntiAFK', 'right_bumper_duration', fallback=0.1)
        self.left_bumper_duration = self.config.getfloat('AntiAFK', 'left_bumper_duration', fallback=0.1)
        self.delay_between_buttons = self.config.getfloat('AntiAFK', 'delay_between_buttons', fallback=0.5)

        # Load Movement settings
        self.min_movement_duration = self.config.getfloat('Movement', 'min_movement_duration', fallback=4.0)
        self.max_movement_duration = self.config.getfloat('Movement', 'max_movement_duration', fallback=6.0)
        self.min_break_duration = self.config.getfloat('Movement', 'min_break_duration', fallback=3.0)
        self.max_break_duration = self.config.getfloat('Movement', 'max_break_duration', fallback=7.0)

    def anti_afk_loop(self):
        """Anti-AFK loop that periodically presses buttons."""
        print("Anti-AFK loop started")
        while self.running:
            if not self.anti_afk_enabled:
                time.sleep(0.1)
                continue

            self.press_rb()
            time.sleep(self.delay_between_buttons)
            self.press_lb()

            print(f"Anti-AFK: Waiting {self.anti_afk_interval} seconds")
            time.sleep(self.anti_afk_interval)
        print("Anti-AFK loop ended")

    def movement_loop(self):
        """Movement loop that simulates random controller inputs."""
        print("Movement loop started")
        while self.running:
            if not self.movement_enabled:
                time.sleep(0.1)
                continue

            print("Simulating movement...")
            duration = random.uniform(self.min_movement_duration, self.max_movement_duration)
            start_time = time.time()

            while self.running and self.movement_enabled and (time.time() - start_time) < duration:
                move_x = random.uniform(-1, 1)
                move_y = random.uniform(-1, 1)
                self.gamepad.left_joystick_float(x_value_float=move_x, y_value_float=move_y)
                self.gamepad.update()
                time.sleep(0.1)

            print(f"Movement phase complete. Breaking for {duration} seconds.")
            time.sleep(random.uniform(self.min_break_duration, self.max_break_duration))
        print("Movement loop ended")

    # Individual Button and Control Methods
    def press_a(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A, "A")

    def press_b(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B, "B")

    def press_x(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X, "X")

    def press_y(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y, "Y")

    def press_lb(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER, "LB")

    def press_rb(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, "RB")

    def press_lt(self):
        self._press_trigger(0, "LT")

    def press_rt(self):
        self._press_trigger(1, "RT")

    def press_start(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START, "START")

    def press_back(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK, "BACK")

    def press_ls(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB, "Left Stick Click")

    def press_rs(self):
        self._press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB, "Right Stick Click")

    def move_dpad_up(self):
        self._move_dpad(vg.DPAD.UP, "DPAD UP")

    def move_dpad_down(self):
        self._move_dpad(vg.DPAD.DOWN, "DPAD DOWN")

    def move_dpad_left(self):
        self._move_dpad(vg.DPAD.LEFT, "DPAD LEFT")

    def move_dpad_right(self):
        self._move_dpad(vg.DPAD.RIGHT, "DPAD RIGHT")

    def move_left_stick(self, x, y):
        self.gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()
        print(f"Moved Left Stick to ({x}, {y})")

    def move_right_stick(self, x, y):
        self.gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
        self.gamepad.update()
        print(f"Moved Right Stick to ({x}, {y})")

    # Helper Methods for Actions
    def _press_button(self, button, name):
        print(f"Pressing '{name}' button")
        self.gamepad.press_button(button)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button)
        self.gamepad.update()

    def _press_trigger(self, trigger, name):
        print(f"Pressing '{name}' trigger")
        if trigger == 0:  # LT
            self.gamepad.left_trigger(value=255)
        elif trigger == 1:  # RT
            self.gamepad.right_trigger(value=255)
        self.gamepad.update()
        time.sleep(0.1)
        if trigger == 0:  # LT
            self.gamepad.left_trigger(value=0)
        elif trigger == 1:  # RT
            self.gamepad.right_trigger(value=0)
        self.gamepad.update()

    def _move_dpad(self, direction, name):
        print(f"Moving '{name}'")
        self.gamepad.d_pad(direction)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.d_pad(vg.DPAD.OFF)
        self.gamepad.update()

    def toggle_mode(self, mode):
        """Switch between Anti-AFK and Movement mode."""
        if mode == "anti_afk":
            self.anti_afk_enabled = True
            self.movement_enabled = False
            print("Switched to Anti-AFK mode")
        elif mode == "movement":
            self.anti_afk_enabled = False
            self.movement_enabled = True
            print("Switched to Movement mode")


class HWIDManager:
    """Manages whitelisted HWIDs using an .ini file."""

    def __init__(self, ini_file="hwid_whitelist.ini"):
        self.ini_file = ini_file
        self.config = configparser.ConfigParser()
        self.load_hwid_list()

    def load_hwid_list(self):
        """Load the whitelist from the .ini file."""
        if not os.path.exists(self.ini_file):
            raise FileNotFoundError(f"HWID file {self.ini_file} not found.")
        self.config.read(self.ini_file)
        self.whitelisted_hwids = set(self.config["WHITELISTED_HWIDS"].values())

    def is_hwid_whitelisted(self, hwid):
        """Check if the provided HWID is in the whitelist."""
        return hwid in self.whitelisted_hwids



class CommandServer:
    """A server that handles client commands and enforces HWID checks."""

    def __init__(self, hwid_manager, host="0.0.0.0", port=9999):
        self.hwid_manager = hwid_manager
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True
        self.gamepad_controller = GamepadController()  # Initialize GamepadController

    def handle_client(self, conn, addr):
        """Handle incoming client commands."""
        print(f"[INFO] Connected to {addr}")
        with conn:
            try:
                # Receive the HWID from the client as the first message
                hwid = conn.recv(1024).decode().strip()
                print(f"[INFO] Received HWID: {hwid}")

                # Validate the HWID
                if not self.hwid_manager.is_hwid_whitelisted(hwid):
                    conn.sendall("HWID not authorized.".encode())
                    print(f"[WARNING] Unauthorized HWID: {hwid}")
                    return

                conn.sendall("HWID authorized.".encode())
                print(f"[INFO] HWID authorized: {hwid}")

                # Process subsequent commands
                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break

                    print(f"[INFO] Received command: {data}")

                    if data == "press_healthcheck":
                        conn.sendall("alive".encode())
                    elif data in self.get_supported_commands():
                        self.execute_gamepad_command(data)
                        conn.sendall(f"Executed command: {data}".encode())
                    elif data == "start_anti_afk":
                        self.start_anti_afk()
                        conn.sendall("Anti-AFK started.".encode())
                    elif data == "stop_anti_afk":
                        self.stop_anti_afk()
                        conn.sendall("Anti-AFK stopped.".encode())
                    elif data == "start_movement":
                        self.start_movement()
                        conn.sendall("Movement started.".encode())
                    elif data == "stop_movement":
                        self.stop_movement()
                        conn.sendall("Movement stopped.".encode())
                    else:
                        conn.sendall("unknown command".encode())

            except Exception as e:
                print(f"[ERROR] Error handling client {addr}: {e}")

    def get_supported_commands(self):
        """Return a list of supported gamepad commands."""
        return [
            "press_a", "press_b", "press_x", "press_y",
            "press_lb", "press_rb", "press_lt", "press_rt",
            "press_up", "press_down", "press_left", "press_right",
            "press_start", "press_back", "press_ls", "press_rs"
        ]

    def execute_gamepad_command(self, command):
        """Execute the corresponding gamepad command."""
        try:
            if command == "press_a":
                self.gamepad_controller.press_a()
            elif command == "press_b":
                self.gamepad_controller.press_b()
            elif command == "press_x":
                self.gamepad_controller.press_x()
            elif command == "press_y":
                self.gamepad_controller.press_y()
            elif command == "press_lb":
                self.gamepad_controller.press_lb()
            elif command == "press_rb":
                self.gamepad_controller.press_rb()
            elif command == "press_lt":
                self.gamepad_controller.press_lt()
            elif command == "press_rt":
                self.gamepad_controller.press_rt()
            elif command == "press_up":
                self.gamepad_controller.move_dpad_up()
            elif command == "press_down":
                self.gamepad_controller.move_dpad_down()
            elif command == "press_left":
                self.gamepad_controller.move_dpad_left()
            elif command == "press_right":
                self.gamepad_controller.move_dpad_right()
            elif command == "press_start":
                self.gamepad_controller.press_start()
            elif command == "press_back":
                self.gamepad_controller.press_back()
            elif command == "press_ls":
                self.gamepad_controller.press_ls()
            elif command == "press_rs":
                self.gamepad_controller.press_rs()
            else:
                print(f"[WARNING] Command '{command}' not implemented.")
        except Exception as e:
            print(f"[ERROR] Failed to execute gamepad command '{command}': {e}")

    def start_anti_afk(self):
        """Start the anti-AFK loop."""
        self.gamepad_controller.anti_afk_enabled = True
        if not hasattr(self, "_anti_afk_thread") or not self._anti_afk_thread.is_alive():
            self._anti_afk_thread = threading.Thread(target=self.gamepad_controller.anti_afk_loop, daemon=True)
            self._anti_afk_thread.start()
        print("[INFO] Anti-AFK started.")

    def stop_anti_afk(self):
        """Stop the anti-AFK loop."""
        self.gamepad_controller.anti_afk_enabled = False
        print("[INFO] Anti-AFK stopped.")

    def start_movement(self):
        """Start the movement loop."""
        self.gamepad_controller.movement_enabled = True
        if not hasattr(self, "_movement_thread") or not self._movement_thread.is_alive():
            self._movement_thread = threading.Thread(target=self.gamepad_controller.movement_loop, daemon=True)
            self._movement_thread.start()
        print("[INFO] Movement started.")

    def stop_movement(self):
        """Stop the movement loop."""
        self.gamepad_controller.movement_enabled = False
        print("[INFO] Movement stopped.")

    def start(self):
        """Start the server."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[INFO] Server listening on {self.host}:{self.port}")

            while self.is_running:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
        except Exception as e:
            print(f"[ERROR] Server encountered an error: {e}")
        finally:
            self.shutdown()

    def shutdown(self):
        """Shutdown the server gracefully."""
        print("[INFO] Shutting down server...")
        self.is_running = False
        self.server_socket.close()


def signal_handler(sig, frame):
    """Handle signals for graceful shutdown."""
    print("[INFO] Received termination signal. Exiting...")
    sys.exit(0)


def log_info(message):
    """Standard log practice for informational messages."""
    print(f"[INFO] {message}")


def log_error(message):
    """Standard log practice for error messages."""
    print(f"[ERROR] {message}")


def log_success(message):
    """Standard log practice for success messages."""
    print(f"[SUCCESS] {message}")


def get_chrome_version():
    """Get the version of installed Google Chrome."""
    log_info("Checking Google Chrome version...")
    try:
        system = platform.system()
        if system == "Windows":
            command = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        elif system == "Darwin":  # macOS
            command = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        elif system == "Linux":
            command = "google-chrome --version"
            version = subprocess.check_output(command, shell=True).decode().strip()
            return version.split()[-1]
        else:
            raise Exception("Unsupported Operating System")
    except Exception as e:
        log_error(f"Could not detect Google Chrome version: {e}")
        raise


def download_chromedriver(chrome_version):
    """Download the ChromeDriver that matches the installed Google Chrome version."""
    try:
        log_info("Determining the correct ChromeDriver version...")
        major_version = chrome_version.split(".")[0]
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        latest_driver_version = requests.get(url).text.strip()

        driver_download_url = f"https://chromedriver.storage.googleapis.com/{latest_driver_version}/chromedriver_{platform.system().lower()}64.zip"
        log_info(f"Downloading ChromeDriver from: {driver_download_url}")

        response = requests.get(driver_download_url, stream=True)
        zip_path = "chromedriver.zip"
        with open(zip_path, "wb") as file:
            file.write(response.content)

        # Extract the downloaded zip
        log_info("Extracting ChromeDriver...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("chromedriver")

        # Clean up
        os.remove(zip_path)
        chromedriver_path = os.path.abspath("chromedriver/chromedriver")
        log_success(f"ChromeDriver downloaded and available at: {chromedriver_path}")
        return chromedriver_path
    except Exception as e:
        log_error(f"Failed to download ChromeDriver: {e}")
        raise


def check_and_install_dependencies():
    """Check and install required dependencies."""
    log_info("Checking required dependencies...")
    try:
        # Check Google Chrome version
        chrome_version = get_chrome_version()
        log_success(f"Google Chrome version detected: {chrome_version}")

        # Check or install ChromeDriver
        if not os.path.exists("chromedriver/chromedriver"):
            log_info("ChromeDriver not found. Downloading...")
            return download_chromedriver(chrome_version)
        else:
            log_success("ChromeDriver already exists.")
            return os.path.abspath("chromedriver/chromedriver")
    except Exception as e:
        log_error(f"Dependency check failed: {e}")
        raise


if __name__ == "__main__":
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


    # Check and install dependencies
    chromedriver_path = check_and_install_dependencies()

    # Load the HWID whitelist
    hwid_manager = HWIDManager()

    # Start the server
    server = CommandServer(hwid_manager)
    server.start()
