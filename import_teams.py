import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("data/Teams.csv")

# Connect to DB
conn = sqlite3.connect("Championship.db")
cur = conn.cursor()

# Clear old data
cur.execute("DELETE FROM league_table")

# Insert rows
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO league_table 
        (team, played, won, drawn, lost, goals_for, goals_against, goal_difference, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["team_name"],
        row["played"],
        row["won"],
        row["drawn"],
        row["lost"],
        row["goals_for"],
        row["goals_against"],
        row["goal_difference"],
        row["points"]
    ))

conn.commit()
conn.close()

print("Teams imported successfully.")