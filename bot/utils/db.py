import sqlite3
from contextlib import closing

def get_db_connection():
    """Creates a new database connection."""
    return sqlite3.connect("lindamatic.db")

def initialize_database():
    """Initializes the SQLite database schema."""
    with closing(get_db_connection()) as conn:
        cursor = conn.cursor()

        # Users Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL,
            county TEXT NOT NULL,
            completed_gates TEXT, -- JSON string of completed gates
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Gates Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gate_name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # User-Gate Progress Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_gate_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            gate_id INTEGER NOT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (gate_id) REFERENCES gates(id)
        )
        ''')

        conn.commit()

def save_user_to_db(telegram_id, first_name, last_name, phone_number, email, county):
    """Saves a user's registration data to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (telegram_id, first_name, last_name, phone_number, email, county, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (telegram_id, first_name, last_name, phone_number, email, county))
        conn.commit()

def get_user_by_telegram_id(telegram_id):
    """Fetches a user's data from the database by their Telegram ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return cursor.fetchone()

def save_gate_to_db(gate_name, description):
    """Saves a new gate to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gates (gate_name, description, created_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (gate_name, description))
        conn.commit()

def get_all_gates():
    """Fetches all gates from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gates')
        return cursor.fetchall()

def save_user_gate_progress(user_id, gate_id):
    """Saves a user's progress for a specific gate."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user_gate_progress (user_id, gate_id, completed_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, gate_id))
        conn.commit()
