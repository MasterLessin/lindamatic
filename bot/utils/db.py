import sqlite3
from contextlib import closing

DATABASE_FILE = "./database/database.db"

def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Return results as dictionaries
    return conn

def initialize_database():
    """Initializes the SQLite database schema."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Clients Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram_id TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Content Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            type TEXT NOT NULL,  -- "file" or "link"
            value TEXT NOT NULL, -- e.g., file path or URL
            gate_type TEXT NOT NULL, -- e.g., "instagram", "tiktok"
            gate_value TEXT NOT NULL, -- e.g., username or group link
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        ''')

        # Updated Users Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL,
            county TEXT NOT NULL,
            completed_gates TEXT DEFAULT '', -- JSON string of completed gates
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        print("Database initialized successfully!")

