import os
import subprocess
import sys
import json
from threading import Thread
from flask import Flask
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from backend.app import create_app

# Constants
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend_ui")
APP_CONFIG_PATH = os.path.join(FRONTEND_DIR, "src", "constants", "appConfig.json")
BACKEND_PORT = 6000
FRONTEND_PORT = 4173
ALLOWED_USER_AGENT = "PySide6-WebEngine"  # Restrict to PySide6


def update_backend_url():
    """Update the backendUrl in frontend's appConfig.json."""
    backend_url = f"http://127.0.0.1:{BACKEND_PORT}"
    app_config = {}

    with open(APP_CONFIG_PATH, "r") as f:
        app_config = json.load(f)

    app_config["backendUrl"] = backend_url

    with open(APP_CONFIG_PATH, "w") as f:
        json.dump(app_config, f, indent=4)

    print(f"Updated backendUrl in appConfig.json to {backend_url}")


def start_backend():
    """Start the Flask backend server."""
    print("Starting Flask backend server...")
    app = create_app()
    app.run(port=BACKEND_PORT, use_reloader=False)


def start_frontend():
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
    window = MainWindow(f"http://localhost:{FRONTEND_PORT}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
