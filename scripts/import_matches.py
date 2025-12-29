# Author: Đani Čolaković
import sqlite3
import csv
import os

# Path to the SQLite Database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Championship.db")

# Path to the CSV file containing match data
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Matches.csv")

# This imports match fixtures from the CSV file into the matches table in the database
def import_matches():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Created matches table if it doesn't exist 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matchday INTEGER,
            home_team TEXT,
            away_team TEXT,
            home_goals INTEGER,
            away_goals INTEGER,
            date TEXT
        )
    """)

    # Cleared old data before importing new match fixtures 
    cursor.execute("DELETE FROM matches")

    # Inserted new EFL Championship match fixture data
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO matches (matchday, home_team, away_team, home_goals, away_goals, date)
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
    print("Matches imported successfully.")

if __name__ == "__main__":
    import_matches()