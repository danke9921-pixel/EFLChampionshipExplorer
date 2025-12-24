# Author: Đani Čolaković
# connect.py
# This is a Simple SQLite Connection Setup

import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database/championship.db")
    conn.row_factory = sqlite3.Row  # allows dict-style access: user["username"]

    # Ensure the 'banned' column exists in the users table
    try:
        conn.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except:
        pass  # Column already exists, ignore the error

    return conn