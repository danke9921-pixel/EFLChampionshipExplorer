# Author: Đani Čolaković
# connect.py
# Simple SQLite connection setup

import sqlite3

def get_connection():
    return sqlite3.connect("database/championship.db")