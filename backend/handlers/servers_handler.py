import sqlite3
from flask import request
from backend.database import get_db_connection
from backend.utils.response_helper import create_response, ResponseType
from backend.utils.server_utils import fetch_server_ips, verify_server_health


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

    # Verify health of each server
    servers_status_with_reason = [
        {"serverIp": ip, "status": status, "reason": reason}
        for ip in servers_to_check
        for status, reason in [verify_server_health(ip)]
    ]

    # Prepare the response
    response = {"serversList": servers_status_with_reason}
    return create_response(ResponseType.SUCCESS, "Server health checked successfully.", response)
