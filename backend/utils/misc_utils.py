import webbrowser
from flask import request
from backend.utils.response_helper import create_response, ResponseType
import os
import hashlib
import platform
import uuid

def open_url_browser():
    """
    Open the target URL in the system's default web browser.

    Expects JSON payload:
    {
        "targetUrl": "http://example.com"
    }
    """
    data = request.get_json()

    # Validate the input
    if not data or "targetUrl" not in data:
        return create_response(
            ResponseType.ERROR, 
            "targetUrl is required", 
            {}, 
            400
        )

    target_url = data["targetUrl"]

    # Open the URL in the system's default browser
    try:
        webbrowser.open(target_url)
        return create_response(
            ResponseType.SUCCESS, 
            f"URL {target_url} opened successfully", 
            {}, 
            200
        )
    except Exception as e:
        return create_response(
            ResponseType.ERROR, 
            f"Failed to open URL: {str(e)}", 
            {}, 
            500
        )


def get_device_hwid():
    """Generate a unique and persistent device HWID."""
    # Collect immutable system-specific data
    mac_address = uuid.getnode()  # Get MAC address (unchanging unless manually altered)
    cpu_info = platform.processor()  # Processor information
    disk_info = None

    # Try to get disk information (platform-dependent)
    try:
        if platform.system() == "Windows":
            disk_info = os.popen("wmic diskdrive get serialnumber").read().strip()
        elif platform.system() == "Darwin":  # macOS
            disk_info = os.popen("ioreg -l | grep IOPlatformSerialNumber").read().strip()
        elif platform.system() == "Linux":
            disk_info = os.popen("lsblk -o SERIAL").read().strip()
    except Exception:
        disk_info = "unknown_disk"

    # Use consistent attributes to form a base identifier
    raw_data = f"{mac_address}-{cpu_info}-{disk_info}"

    # Hash the identifier using SHA-256 for consistency and security
    hwid_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    return hwid_hash

