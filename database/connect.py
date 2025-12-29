# Author: Đani Čolaković
# connect.py
# This is a Simple SQLite Connection Setup
import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), "..", "Championship.db")
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection