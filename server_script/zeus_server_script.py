import os
import configparser
import socket
import threading
import sys
import signal


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

                    if data == "healthCheck":
                        conn.sendall("alive".encode())
                    else:
                        conn.sendall("unknown command".encode())

            except Exception as e:
                print(f"[ERROR] Error handling client {addr}: {e}")

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


if __name__ == "__main__":
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Load the HWID whitelist
    hwid_manager = HWIDManager()

    # Start the server
    server = CommandServer(hwid_manager)
    server.start()
