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
from backend.app import create_app

# Constants
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend_ui")
APP_CONFIG_PATH = os.path.join(FRONTEND_DIR, "src", "constants", "appConfig.json")
BACKEND_PORT = 5000
FRONTEND_PORT = 4173
ALLOWED_USER_AGENT = "PySide6-WebEngine"  # Restrict to PySide6


def is_port_available(port):
    """Check if a port is available on the system."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
        return result != 0  # 0 means the port is in use


def find_available_port(start_port):
    """Find the next available port starting from the given port number."""
    port = start_port
    while not is_port_available(port):
        port += 1
    return port


def update_backend_url(backend_port):
    """Update the backendUrl in frontend's appConfig.json."""
    backend_url = f"http://127.0.0.1:{backend_port}"
    app_config = {}

    with open(APP_CONFIG_PATH, "r") as f:
        app_config = json.load(f)

    app_config["backendUrl"] = backend_url

    with open(APP_CONFIG_PATH, "w") as f:
        json.dump(app_config, f, indent=4)

    print(f"Updated backendUrl in appConfig.json to {backend_url}")


def start_backend(backend_port):
    """Start the Flask backend server."""
    print(f"Starting Flask backend server on port {backend_port}...")
    app = create_app()
    app.run(port=backend_port, use_reloader=False)


def start_frontend(frontend_port):
    """Start the Vue.js frontend server."""
    print("Checking Vue.js frontend setup...")

    if not os.path.exists(os.path.join(FRONTEND_DIR, "node_modules")):
        print("Node modules not found. Installing...")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    print("Building Vue.js frontend...")
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("Starting Vue.js frontend preview server...")
    subprocess.Popen(["npm", "run", "serve"], cwd=FRONTEND_DIR)


class MainWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Zeus Manager Cod Bo6 Bot Lobby")
        self.setFixedSize(1024, 768)  # Fixed tablet resolution
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))  # Restrict access to embedded browser
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


def main():
    # Find available ports for backend and frontend
    available_backend_port = find_available_port(BACKEND_PORT)
    available_frontend_port = find_available_port(FRONTEND_PORT)

    # Update the backend URL in frontend config with the available backend port
    update_backend_url(available_backend_port)

    # Start the backend first
    backend_thread = Thread(target=start_backend, args=(available_backend_port,), daemon=True)
    backend_thread.start()

    # Wait a moment to ensure backend is ready
    import time
    time.sleep(3)

    # Start the frontend
    start_frontend(available_frontend_port)

    # Start the PySide6 application
    app = QApplication(sys.argv)
    window = MainWindow(f"http://localhost:{available_frontend_port}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
