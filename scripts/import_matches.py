# Author: Đani Čolaković
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Championship.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "Matches.csv")

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DELETE FROM matches")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO matches
        (matchday, home_team, away_team, home_goals, away_goals, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(row["matchday"]),
        row["home_team"],
        row["away_team"],
        int(row["home_goals"]),
        int(row["away_goals"]),
        row["date"]
    ))

conn.commit()
conn.close()

print(" Matches table updated.")