# Author: Đani Čolaković
# Login + registration system with bcrypt hashing

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import bcrypt
from database.connect import get_db_connection


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def authenticate(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, password, favourite_team, banned FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    connection.close()

    if user:
        # Block banned users
        if user["banned"] == 1:
            return "banned"

        stored_hash = user["password"]

        if verify_password(password, stored_hash):
            role = "admin" if username == "admin" else "fan"
            return {
                "username": user["username"],
                "favourite_team": user["favourite_team"],
                "role": role
            }

    return None


def register_user(username, password, favourite_team=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )
    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False

    hashed = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, password, favourite_team, banned) VALUES (?, ?, ?, 0)",
        (username, hashed, favourite_team)
    )

    connection.commit()
    connection.close()
    return True