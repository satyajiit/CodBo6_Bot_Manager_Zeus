from datetime import datetime
from enum import Enum
from flask import jsonify


class ResponseType(Enum):
    SUCCESS = "OK"
    ERROR = "NOT-OK"


def create_response(response_type: ResponseType, message: str, data: dict = None, status_code: int = 200):
    """Create a standardized JSON response.

    Args:
        response_type (ResponseType): Enum indicating success or error.
        message (str): Message to include in the response.
        data (dict, optional): Additional data to include in the response.
        status_code (int): HTTP status code for the response.

    Returns:
        Response: Flask JSON response object with status code.
    """
    response = {
        "status": response_type.value,
        "message": message,
        "data": data if data is not None else {},
        "timestamp": int(datetime.utcnow().timestamp()),  # UTC timestamp in seconds
    }
    return jsonify(response), status_code
