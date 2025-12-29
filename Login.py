# Author: Đani Čolaković
# Login.py 
# Handles user authenticatio and registration using bcrypt hashing 

import sys
from pathlib import Path
# Add project root to Python path so imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

import re
import bcrypt
from database.connect import get_db_connection

# Password Validation
def is_valid_password(password: str) -> bool:

    # Checks if the password meets basic security requirements
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Password Hashing and Verification 
def hash_password(password: str) -> bytes:
    # This hashes a password using bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

# User Authentication 
def authenticate(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT username, password, favourite_team, banned, role FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    connection.close()

    if user:
        # Block banned users immediately 
        if user["banned"] == 1:
            return "banned"

        stored_hash = user["password"]
        # Verify password hash 

        if verify_password(password, stored_hash):
            return {
                "username": user["username"],
                "favourite_team": user["favourite_team"],
                "role": user["role"]  # role from DB
            }

    return None

# User Registration 
def register_user(username, password, favourite_team=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if username already exists
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )
    existing = cursor.fetchone()

    if existing:
        connection.close()
        return False, "username_exists"

    # Validate password strength 
    if not is_valid_password(password):
        connection.close()
        return False, "weak_password"

    hashed = hash_password(password)

    #  Check if an admin already exists
    cursor.execute("SELECT COUNT(*) AS count FROM users WHERE role = 'admin'")
    admin_exists = cursor.fetchone()["count"] > 0

    # First registered user becomes admin
    role = "admin" if not admin_exists else "user"

    cursor.execute(
        "INSERT INTO users (username, password, favourite_team, banned, role) VALUES (?, ?, ?, 0, ?)",
        (username, hashed, favourite_team, role)
    )

    connection.commit()
    connection.close()
    return True, "success"