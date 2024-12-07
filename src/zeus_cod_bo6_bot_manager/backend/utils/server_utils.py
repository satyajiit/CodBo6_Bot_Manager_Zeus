import os

from zeus_cod_bo6_bot_manager.backend.database import get_db_connection
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from zeus_cod_bo6_bot_manager.backend.utils.misc_utils import get_device_hwid

CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config", "servers.in")




def fetch_server_ips():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all IPs from the database
    cursor.execute("SELECT ip_address FROM servers")
    servers = [{"serverIp": row[0]} for row in cursor.fetchall()]

    conn.close()

    return servers


class ServerCommunicationError(Exception):
    """Custom exception for server communication errors."""
    pass


def call_server(server_ip, server_port, command, timeout=2):
    """
    Connect to a server, authenticate using HWID, and send a command.

    Args:
        server_ip (str): The IP address of the server.
        server_port (int): The port on which the server is listening.
        command (str): The command to send to the server.
        timeout (int): Connection timeout in seconds.

    Returns:
        str: The response from the server.

    Raises:
        ServerCommunicationError: If communication with the server fails or times out.
    """
    try:
        # Create a socket connection with timeout
        with socket.create_connection((server_ip, server_port), timeout) as conn:
            # Send the HWID as the first message for authentication
            conn.sendall(get_device_hwid().encode())
            auth_response = conn.recv(1024).decode()

            if "authorized" not in auth_response.lower():
                raise ServerCommunicationError(f"HWID not authorized by server: {auth_response}")

            # Send the actual command after successful authentication
            conn.sendall(command.encode())
            response = conn.recv(1024).decode()
            return response
    except socket.timeout:
        raise ServerCommunicationError(f"Timeout: Server {server_ip}:{server_port} is not responding.")
    except Exception as e:
        raise ServerCommunicationError(f"Error communicating with server {server_ip}:{server_port}: {str(e)}")

def verify_server_health(server_ip, server_port=9999):
    """
    Verify the health of a server by sending a health check command with HWID authentication.

    Args:
        server_ip (str): The server IP to check.
        server_port (int): The server port to check.

    Returns:
        tuple: (status, reason) - status can be "healthy" or "unhealthy", reason provides additional info.
    """
    try:
        response = call_server(server_ip, server_port, "healthCheck", timeout=2)
        if response == "alive":
            return "healthy", "Server is responding."
        else:
            return "unhealthy", f"Unexpected response: {response}"
    except ServerCommunicationError as e:
        return "unhealthy", str(e)


def check_all_servers_health(servers_to_check):
    """
    Check the health of multiple servers in parallel.

    Args:
        servers_to_check (set): Set of server IPs to check.

    Returns:
        list: A list of server statuses with reasons.
    """
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of threads as needed
        future_to_server = {executor.submit(verify_server_health, ip): ip for ip in servers_to_check}

        for future in as_completed(future_to_server):
            server_ip = future_to_server[future]
            try:
                status, reason = future.result()
                results.append({"serverIp": server_ip, "status": status, "reason": reason})
            except Exception as e:
                results.append({"serverIp": server_ip, "status": "unhealthy", "reason": str(e)})

    return results
