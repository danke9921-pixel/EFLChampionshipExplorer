# Author: Đani Čolaković
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Championship.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "goals.csv")

df = pd.read_csv(CSV_PATH)

def parse_minute(value):
    s = str(value)
    if "+" in s:
        base, extra = s.split("+")
        return int(base) + int(extra)
    return int(s)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DELETE FROM goals")

for _, row in df.iterrows():
    minute = parse_minute(row["minute"])
    cur.execute("""
        INSERT INTO goals (match_id, team, player, minute, type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        int(row["match_id"]),
        row["team"],
        row["player"],
        minute,
        row["type"]
    ))

conn.commit()
conn.close()

print(" Goals table updated.")