import os
import subprocess
import sys
import json
import socket
from threading import Thread
import platform
import ctypes
import shutil
import threading
from threading import Event
import re





from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend_ui")
APP_CONFIG_PATH = os.path.join(FRONTEND_DIR, "src", "constants", "appConfig.json")
ALLOWED_USER_AGENT = "PySide6-WebEngine"  # Restrict to PySide6

backend_port = None
frontend_port = None
vue_process = None
port_event = Event()  # Event to signal port detection



def find_free_port():
    """Find an available port on the system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def update_backend_url():
    """Update the backendUrl in frontend's appConfig.json."""
    backend_url = f"http://127.0.0.1:{backend_port}"

    with open(APP_CONFIG_PATH, "r") as f:
        app_config = json.load(f)

    app_config["backendUrl"] = backend_url

    with open(APP_CONFIG_PATH, "w") as f:
        json.dump(app_config, f, indent=4)

    print(f"Updated backendUrl in appConfig.json to {backend_url}")


def start_backend():
    """Start the Flask backend server."""
    from zeus_cod_bo6_bot_manager.backend.app import create_app

    global backend_port
    backend_port = find_free_port()
    print(f"Starting Flask backend server on port {backend_port}...")
    app = create_app()
    app.run(port=backend_port, use_reloader=False)


def check_node_installed():
    """Check if Node.js is installed."""
    try:
        # Try to get the Node.js version
        result = subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print(f"Node.js is installed. Version: {result.stdout.decode().strip()}")
        return True
    except FileNotFoundError:
        print("Node.js is not installed.")
        return False


def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_with_admin():
    """Restart the script with administrative privileges."""
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def install_node():
    """Install the latest LTS version of Node.js based on the platform and architecture."""
    print("Installing Node.js...")

    if sys.platform == "win32":
        # Determine system architecture

        if not is_admin():
            print("Re-running script with admin privileges...")
            print("[NOTE]Will try to install NodeJs but if anything fails, better start the script again with admin privileges.")
            restart_with_admin()
            sys.exit()

        arch = platform.machine()
        if arch == "AMD64":
            installer_url = "https://nodejs.org/dist/v20.9.0/node-v20.9.0-x64.msi"
        elif arch == "ARM64":
            installer_url = "https://nodejs.org/dist/v20.9.0/node-v20.9.0-arm64.msi"
        else:
            raise OSError(f"Unsupported architecture on Windows: {arch}")

        # Download and install Node.js
        installer_path = os.path.join(os.getcwd(), "node-installer.msi")
        try:
            print(f"Downloading Node.js installer from {installer_url}...")
            subprocess.run(["curl", "-o", installer_path, installer_url], check=True)
            print("Running Node.js MSI installer...")
            subprocess.run(["msiexec", "/i", installer_path, "/quiet", "/norestart"], check=True)
            print("Node.js installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"MSI installation failed with error code {e.returncode}. Trying fallback installation.")
            install_node_fallback()

    elif sys.platform in ["linux", "darwin"]:  # Linux or macOS
        # Install Node.js using nvm (Node Version Manager)
        arch = platform.machine()
        if arch not in ["x86_64", "aarch64", "arm64"]:
            raise OSError(f"Unsupported architecture on {sys.platform}: {arch}")

        # Use nvm for cross-architecture support
        subprocess.run(["curl", "-o-", "https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh"], check=True,
                       shell=True)
        subprocess.run(["bash", "-c", ". ~/.nvm/nvm.sh && nvm install --lts"], check=True, shell=True)
        print("Node.js installed successfully!")

    else:
        raise OSError("Unsupported platform for automated Node.js installation. Please install Node.js manually.")


def install_node_fallback():
    """Fallback installation: Download and extract Node.js without MSI."""
    print("Install nodejs manually. Too lazy to support more alternatives!")

def get_updated_env():
    """Update the PATH environment variable to include Node.js, if necessary."""
    env = os.environ.copy()

    # Check if `npm` is already available
    npm_path = shutil.which("npm")
    if npm_path:
        print(f"npm found at: {npm_path}")
        env["PATH"] = f"{os.path.dirname(npm_path)};{env['PATH']}"
        env["npm"] = npm_path  # Add explicit npm path for subprocess
        return env

    # Add default Node.js path to PATH if `npm` is not found
    node_path = "C:\\Program Files\\nodejs"  # Default installation path on Windows
    print("npm not found in PATH. Adding default Node.js path to PATH...")
    env["PATH"] = f"{node_path};{env['PATH']}"

    # Recheck if npm is now available
    npm_path = shutil.which("npm", path=env["PATH"])
    if not npm_path:
        raise FileNotFoundError("npm is not available even after adding Node.js to PATH.")
    env["npm"] = npm_path  # Add explicit npm path for subprocess
    return env


def run_npm_command(command, cwd, env):
    """Run an npm command cross-platform."""
    if sys.platform == "win32":
        # Use cmd.exe on Windows
        npm_path = shutil.which("npm", path=env["PATH"])
        if not npm_path:
            raise FileNotFoundError("npm not found in the updated PATH.")
        subprocess.run(["cmd.exe", "/c", npm_path] + command, cwd=cwd, check=True, env=env)
    else:
        # Use npm directly on Unix-like systems
        subprocess.run(["npm"] + command, cwd=cwd, check=True, env=env)

def set_frontend_port(port):
    """Set the frontend port globally and signal the event."""
    global frontend_port
    frontend_port = port
    print(f"[DEBUG] set_frontend_port called with port: {frontend_port}")
    port_event.set()


def read_output(pipe, log_prefix, port_callback=None):
    """Read output from a subprocess pipe and log it.

    Args:
        pipe: The pipe to read from (stdout or stderr).
        log_prefix: A prefix for log messages (e.g., "STDOUT").
        port_callback: A function to call with the detected port.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    for line in iter(pipe.readline, ''):
        decoded_line = line.strip()
        print(f"{log_prefix}: {decoded_line}")

        # Detect the port dynamically
        if port_callback and "http://localhost" in decoded_line:
            try:
                # Extract the port using split
                port_string = decoded_line.split(":")[-1].strip().rstrip("/")
                port_string = port_string.replace(" ", "").replace("/", "")
                print(f"Detected server port before clearing: {port_string}")
                port_string = ansi_escape.sub('', port_string)  # Remove ANSI sequences
                print(f"Detected server port: {port_string}")
                port = int(port_string)
                port_callback(port)
            except ValueError as e:
                print(f"Error parsing port from line: {decoded_line} - {e}")
    pipe.close()




def start_frontend():
    """Start the Vue.js frontend server."""
    global vue_process

    print("Checking Node.js installation...")
    if not check_node_installed():
        install_node()

    print("Checking Vue.js frontend setup...")

    if not os.path.exists(FRONTEND_DIR):
        print(f"Error: FRONTEND_DIR path does not exist: {FRONTEND_DIR}")
        sys.exit(1)

    try:
        env = get_updated_env()  # Get the environment with `npm` configured
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure Node.js and npm are correctly installed.")
        sys.exit(1)

    if not os.path.exists(os.path.join(FRONTEND_DIR, "node_modules")):
        print("Node modules not found. Installing...")
        run_npm_command(["install"], cwd=FRONTEND_DIR, env=env)

    print("Building Vue.js frontend...")
    run_npm_command(["run", "build"], cwd=FRONTEND_DIR, env=env)

    print("Starting Vue.js frontend preview server...")
    vue_process = subprocess.Popen(
        ["npm", "run", "serve"] if sys.platform != "win32" else ["cmd.exe", "/c", "npm", "run", "serve"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True  # Decode output directly as text
    )

    # Start threads to read stdout and stderr
    threading.Thread(target=read_output, args=(vue_process.stdout, "STDOUT", set_frontend_port), daemon=True).start()
    threading.Thread(target=read_output, args=(vue_process.stderr, "STDERR"), daemon=True).start()

    # Wait for the port to be detected
    print("Waiting for the Vue.js server to start...")
    timeout = 30  # Timeout in seconds
    if not port_event.wait(timeout):  # Wait for the event to be set
        print("Error: Vue.js server did not start within the timeout period.")
        vue_process.terminate()
        sys.exit(1)

    print(f"Vue.js server successfully started on port {frontend_port}")


class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Zeus Manager Cod Bo6 Bot Lobby")
        self.setFixedSize(1400, 768)  # Fixed tablet resolution
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


def cleanup():
    """Clean up processes and resources on script exit."""
    global vue_process
    if vue_process:
        print("Stopping Vue.js frontend server...")
        vue_process.terminate()
    print("All processes terminated.")


def main():
    import signal
    import atexit

    # Ensure cleanup is performed when the script exits
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    # Start the backend first
    backend_thread = Thread(target=start_backend, daemon=True)
    backend_thread.start()

    # Wait a moment to ensure backend is ready
    import time
    time.sleep(3)

    # Update the backend URL in the frontend config
    update_backend_url()

    # Start the frontend
    start_frontend()

    # Start the PySide6 application
    app = QApplication(sys.argv)
    window = MainWindow(f"http://localhost:{frontend_port}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
