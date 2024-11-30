import configparser
import os

from backend.database import get_db_connection

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "servers.in")


def verify_server_health(ip):
    return "Server health check successful!", "OK"

def fetch_server_ips():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all IPs from the database
    cursor.execute("SELECT ip_address FROM servers")
    servers = [{"serverIp": row[0]} for row in cursor.fetchall()]

    conn.close()

    return servers