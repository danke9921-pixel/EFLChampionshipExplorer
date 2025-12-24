# Author: Đani Čolaković
# Login + registration system with bcrypt hashing

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
import bcrypt
from database.connect import get_db_connection


def is_valid_password(password: str) -> bool:
    # At least 8 characters
    if len(password) < 8:
        return False

    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # At least one digit
    if not re.search(r"[0-9]", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


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

    # Check if username exists
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )
    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False, "username_exists"

    # Password validation
    if not is_valid_password(password):
        connection.close()
        return False, "weak_password"

    # Hash password
    hashed = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, password, favourite_team, banned) VALUES (?, ?, ?, 0)",
        (username, hashed, favourite_team)
    )

    connection.commit()
    connection.close()
    return True, "success"