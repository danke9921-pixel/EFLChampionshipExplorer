import sqlite3

connection = sqlite3.connect("Championship.db")
cursor = connection.cursor()

# USERS TABLE
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

# LEAGUE TABLE (example structure — adjust if yours is different)
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