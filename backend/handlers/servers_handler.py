import sqlite3

from flask import request

from backend.database import get_db_connection
from backend.utils.response_helper import create_response, ResponseType
from backend.utils.server_utils import fetch_server_ips, check_all_servers_health, call_server

# Define the available commands (from GamepadController)
SUPPORTED_SERVER_COMMANDS = [
    "start_anti_afk", "stop_anti_afk", "start_movement", "stop_movement",
    "press_a", "press_b", "press_x", "press_y",
    "press_lb", "press_rb", "press_lt", "press_rt",
    "press_dpad_up", "press_dpad_down", "press_dpad_left", "press_dpad_right",
    "press_start", "press_back", "press_ls", "press_rs"
]

def delete_servers():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return create_response(ResponseType.ERROR, "Invalid payload", {})

    servers_to_delete = {entry.get("serverIp") for entry in data if "serverIp" in entry}
    if not servers_to_delete:
        return create_response(ResponseType.ERROR, "No valid server IPs provided", {})

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the provided IPs
    deleted_servers = []
    for ip in servers_to_delete:
        cursor.execute("DELETE FROM servers WHERE ip_address = ?", (ip,))
        if cursor.rowcount > 0:
            deleted_servers.append(ip)

    conn.commit()
    conn.close()

    return create_response(ResponseType.SUCCESS, "Server(s) deleted successfully!", {"deleted": deleted_servers})

def get_servers():
    servers = fetch_server_ips()
    return create_response(ResponseType.SUCCESS, "Servers fetched successfully", servers)


def add_servers():
    """Handler for /addServers endpoint."""
    data = request.get_json()

    if not data or not isinstance(data, list):
        return create_response(ResponseType.ERROR, "Invalid payload", {})

    new_servers = {entry.get("serverIp") for entry in data if "serverIp" in entry}
    if not new_servers:
        return create_response(ResponseType.ERROR, "No valid server IPs provided", {})

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert new IPs, ignoring duplicates
    added_servers = []
    for ip in new_servers:
        try:
            cursor.execute("INSERT INTO servers (ip_address) VALUES (?)", (ip,))
            added_servers.append(ip)
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    conn.close()

    return create_response(ResponseType.SUCCESS, "Servers updated successfully", {"added": added_servers})


def check_server_health():
    """
    Check if a list of servers is reachable and return their health status.
    """
    # Extract data from the request
    data = request.get_json()

    # Validate the payload
    if not isinstance(data, list):
        return create_response(ResponseType.ERROR, "Invalid payload. Expected a list of servers.", {})

        # Extract server IPs to check
    servers_to_check = {entry.get("serverIp") for entry in data if "serverIp" in entry}
    if not servers_to_check:
        return create_response(ResponseType.ERROR, "No valid server IPs provided.", {})

    # Perform parallel health checks
    servers_status_with_reason = check_all_servers_health(servers_to_check)

    # Prepare the response
    response = {"serversList": servers_status_with_reason}
    return create_response(ResponseType.SUCCESS, "Server health checked successfully.", response)

def do_basic_validation(data):
    # Validate the request payload
    if not isinstance(data, dict):
        return create_response(ResponseType.ERROR, "Invalid payload format. Expected a JSON object.", {})

    key_code = data.get("command")
    if not key_code or key_code not in SUPPORTED_SERVER_COMMANDS:
        return create_response(
            ResponseType.ERROR,
            f"Invalid or unsupported command. Supported commands: {SUPPORTED_SERVER_COMMANDS}",
            {}
        )

    servers = data.get("servers", None)  # Optional
    if not isinstance(servers, list):
        return create_response(ResponseType.ERROR, "Invalid servers format. Expected a list of server IPs.", {})

    return servers, key_code


def send_commands_to_target_vm():
    """
    Send commands to specified servers or all servers if no specific server is provided.

    Request Payload:
    {
        "servers": ["serverIp1", "serverIp2"],  # Optional. If not provided, all servers are targeted.
        "keyCode": "press_a"  # Required. The command to send.
    }

    Returns:
        JSON response indicating success or failure for each server.
    """
    servers, command = do_basic_validation(request.get_json())
    results = []
    for server in servers:
        try:
            response = call_server(server["serverIp"], 9999, command)
            results.append({"serverIp": server["serverIp"], "status": "success", "response": response})
        except Exception as e:
            results.append({"serverIp": server["serverIp"], "status": "error", "error": str(e)})

    # Return the result
    return create_response(ResponseType.SUCCESS, "All commands passed to the target VMs.", {"results": results})