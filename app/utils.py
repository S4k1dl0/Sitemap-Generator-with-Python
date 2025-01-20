import sqlite3
from datetime import datetime
from app.database import get_db_connection

def log_action(action, details):
    """Log an action with details into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (action, details) VALUES (?, ?)', (action, details))
    conn.commit()
    conn.close()