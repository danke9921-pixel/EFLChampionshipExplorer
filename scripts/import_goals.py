# Author: Đani Čolaković
import sqlite3
import csv
import os

# Path to the SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Championship.db")

# Path to the CSV file containing goal data
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Goals.csv")

def import_goals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Created goals table  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER,
            team TEXT,
            player TEXT,
            minute INTEGER,
            type TEXT,
            FOREIGN KEY (match_id) REFERENCES matches(id)
        )
    """)

    # Cleared old data before inserting new rows
    cursor.execute("DELETE FROM goals")

    # Insert goal events from the CSV file
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT INTO goals (match_id, team, player, minute, type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                int(row["match_id"]),
                row["team"],
                row["player"],
                int(row["minute"]),
                row["type"]
            ))

    conn.commit()
    conn.close()
    print("Goals imported successfully.")

if __name__ == "__main__":
    import_goals()