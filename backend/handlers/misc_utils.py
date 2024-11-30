import webbrowser
from flask import request
from backend.utils.response_helper import create_response, ResponseType


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
