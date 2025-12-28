import sqlite3
import csv

# Path to my SQLite Database
DB_PATH = "Championship.db"

# Path that matches my Matches CSV
CSV_PATH = "data/Matches.csv"

def import_matches():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Created matches table so that it can store match fixture data 
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

    # Cleared out old data before importing new data 
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