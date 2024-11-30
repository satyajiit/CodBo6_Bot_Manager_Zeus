import os
import hashlib
import platform
import uuid
import pyperclip
from flask import request

from backend.utils.misc_utils import get_device_hwid
from backend.utils.response_helper import create_response, ResponseType

def copy_to_clipboard(): # pragma: no cover
    """Copy the provided text to the clipboard."""
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return create_response(ResponseType.ERROR, "Invalid payload", {})

        text = data.get("text")
        if not text:
            return create_response(ResponseType.ERROR, "No text provided", {})

        pyperclip.copy(text)
        return create_response(ResponseType.SUCCESS, "Text copied to clipboard successfully", {})
    except Exception as e:
        return create_response(ResponseType.ERROR, f"Failed to copy text to clipboard: {str(e)}", {})

def get_hwid():
    try:
        hwid = get_device_hwid()
        return create_response(ResponseType.SUCCESS, "Device HWID fetched successfully.", {"hwid": hwid})
    except Exception as e:
        return create_response(ResponseType.ERROR, f"Failed to fetch device HWID: {str(e)}", {})

