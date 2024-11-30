import configparser
import os
from backend.utils.server_utils import read_server_ips
from flask import jsonify, request

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "servers.in")


def get_servers():
    """Handler for /servers endpoint."""
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE_PATH)

    # Read server IPs from the 'Servers' section
    servers = [{"serverIp": ip} for ip in config.options("Servers")]
    return jsonify(servers), 200


def add_servers():
    """Handler for /addServers endpoint."""
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid payload"}), 400

    new_servers = {entry.get("serverIp") for entry in data if "serverIp" in entry}
    if not new_servers:
        return jsonify({"error": "No valid server IPs provided"}), 400

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE_PATH)

    # Add new server IPs without duplication
    existing_servers = set(config.options("Servers"))
    updated_servers = existing_servers.union(new_servers)

    # Convert IPs to a dictionary with empty string values (configparser requires this)
    config["Servers"] = {ip: "" for ip in updated_servers}  # Keys and values must be strings

    # Write back to the config file
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as configfile:
        config.write(configfile)

    return jsonify({
        "message": "Servers updated successfully",
        "added": list(new_servers - existing_servers)
    }), 200

def check_server_health():
    """Handler for /checkServerHealth endpoint."""
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE_PATH)

    server_ips = read_server_ips()
    if not server_ips:
        return jsonify({
            "message": "Servers health report",
            "servers": list()
        }), 200

    servers_status = []
    for server_ip in server_ips:
        server_status = {
            "server_ip": server_ip,
            "status": "unknown"
        }

        # Use the dummy health check method
        health_status = "ok"

        if health_status == "ok":
            server_status["status"] = "healthy"
        else:
            server_status["status"] = "unhealthy"

        servers_status.append(server_status)

    return jsonify({
        "message": "Servers health report",
        "servers": servers_status
    }), 200



