# Author: Đani Čolaković
# Login.py
# Basic login and registration system (no hashing yet)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.connect import get_connection


def authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, password, favourite_team FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    connection.close()

    if user and user["password"] == password:
        role = "admin" if username == "admin" else "fan"
        return {
            "username": user["username"],
            "favourite_team": user["favourite_team"],
            "role": role
        }

    return None


def register_user(username, password, favourite_team=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )
    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False

    cursor.execute(
        "INSERT INTO users (username, password, favourite_team) VALUES (?, ?, ?)",
        (username, password, favourite_team)
    )

    connection.commit()
    connection.close()
    return True