from flask import Flask
from backend.endpoints import register_routes
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Allow CORS for the frontend
    CORS(app, resources={r"/*": {"origins": r"http://localhost:\d+"}})

    register_routes(app)
    return app
