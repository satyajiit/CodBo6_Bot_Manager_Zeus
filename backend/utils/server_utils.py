import configparser
import os

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "servers.in")

def read_server_ips():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE_PATH)

    # Check if the "Servers" section exists
    if "Servers" in config:
        # Retrieve all keys (IPs) from the "Servers" section
        server_ips = set(config.options("Servers"))
        return server_ips
    else:
        return set()