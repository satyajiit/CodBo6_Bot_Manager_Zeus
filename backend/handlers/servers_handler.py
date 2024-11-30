import sqlite3
from flask import request
from backend.database import get_db_connection
from backend.utils.response_helper import create_response, ResponseType


def get_servers():
    """Handler for /servers endpoint."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all IPs from the database
    cursor.execute("SELECT ip_address FROM servers")
    servers = [{"serverIp": row[0]} for row in cursor.fetchall()]

    conn.close()
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
