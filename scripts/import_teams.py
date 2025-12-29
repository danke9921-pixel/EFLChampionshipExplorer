# Author: Đani Čolaković
import sqlite3
import pandas as pd
import os

# Path to the CSV file containing the league table data
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Teams.csv")

# Path to the SQlite Database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Championship.db")
# Load the CSV into a DataFrame
df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Remove old league table data before inserting new rows 
cur.execute("DELETE FROM league_table")

# Insert each row from the CSV into the database 
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
# Save changes and close the connection 
conn.commit()
conn.close()

print("Teams imported successfully.")