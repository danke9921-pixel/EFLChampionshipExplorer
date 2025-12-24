# Author: Đani Čolaković
# connect.py
# This is a Simple SQLite Connection Setup
import sqlite3

def get_db_connection():
    connection = sqlite3.connect("Championship.db")
    connection.row_factory = sqlite3.Row
    return connection