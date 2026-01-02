# Author: Đani Čolaković
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Championship.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "Teams.csv")

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS teams")
cur.execute("""
    CREATE TABLE teams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_name TEXT UNIQUE NOT NULL
    )
""")

for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO teams (team_name) VALUES (?)",
        (row["team_name"],)
    )

conn.commit()
conn.close()

print(" Teams table created and populated.")