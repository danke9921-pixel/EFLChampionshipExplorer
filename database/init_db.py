# Author: Đani Čolaković
import sqlite3
import os

# Correct path to database (root folder)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Championship.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# This creates the User table 
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB,
    favourite_team TEXT,
    banned INTEGER DEFAULT 0,
    role TEXT
)
""")

# Create table for storing league standings
cursor.execute("""
CREATE TABLE IF NOT EXISTS league_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team TEXT,
    played INTEGER,
    won INTEGER,
    drawn INTEGER,
    lost INTEGER,
    goals_for INTEGER,
    goals_against INTEGER,
    goal_difference INTEGER,
    points INTEGER
)
""")

connection.commit()
connection.close()

print("Database and tables created successfully.")