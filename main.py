import os
import subprocess
import sys
import json
import socket
from threading import Thread
from flask import Flask
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

# Constants
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend_ui")
APP_CONFIG_PATH = os.path.join(FRONTEND_DIR, "src", "constants", "appConfig.json")
ALLOWED_USER_AGENT = "PySide6-WebEngine"  # Restrict to PySide6

backend_port = None
frontend_port = None
vue_process = None


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
    from backend.app import create_app

    global backend_port
    backend_port = find_free_port()
    print(f"Starting Flask backend server on port {backend_port}...")
    app = create_app()
    app.run(port=backend_port, use_reloader=False)


def start_frontend():
    """Start the Vue.js frontend server."""
    global frontend_port, vue_process

    print("Checking Vue.js frontend setup...")
    if not os.path.exists(os.path.join(FRONTEND_DIR, "node_modules")):
        print("Node modules not found. Installing...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    print("Building Vue.js frontend...")
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("Starting Vue.js frontend preview server...")
    vue_process = subprocess.Popen(
        ["npm", "run", "serve"], cwd=FRONTEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Detect Vue.js server port dynamically
    while True:
        line = vue_process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode("utf-8").strip()
        if "Local:" in decoded_line:
            # Extract the port from the line, removing any trailing slashes
            port_string = decoded_line.split(":")[-1].strip().rstrip("/")
            try:
                frontend_port = int(port_string)
                print(f"Vue.js server started on port {frontend_port}")
                break
            except ValueError:
                print(f"Error parsing port from line: {decoded_line}")


class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Zeus Manager Cod Bo6 Bot Lobby")
        self.setFixedSize(1024, 768)  # Fixed tablet resolution
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

    # Start the frontend
    start_frontend()

    # Update the backend URL in the frontend config
    update_backend_url()

    # Start the PySide6 application
    app = QApplication(sys.argv)
    window = MainWindow(f"http://localhost:{frontend_port}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
