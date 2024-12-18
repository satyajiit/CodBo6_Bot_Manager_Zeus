from flask import Flask
from zeus_cod_bo6_bot_manager.backend.endpoints import register_routes
from flask_cors import CORS
from zeus_cod_bo6_bot_manager.backend.database import init_db


def create_app():
    app = Flask(__name__)

    # Initialize SQLite database
    init_db()

    # Allow CORS for the frontend
    CORS(app, resources={r"/*": {"origins": [r"http://127.0.0.1:\d+", r"http://localhost:\d+"]}})

    register_routes(app)
    return app
