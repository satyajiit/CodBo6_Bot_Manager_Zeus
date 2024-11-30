import os
import sqlite3

DB_PATH = os.path.join(os.getcwd(), "config", "servers.db")


def init_db():
    """Initialize the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the servers table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    """Get a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)
