"""
Database connection and initialization
"""

import sqlite3
import os

DATABASE_PATH = "./database/hospital.db"

def get_db_connection():
    """Get database connection."""
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database directory."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

