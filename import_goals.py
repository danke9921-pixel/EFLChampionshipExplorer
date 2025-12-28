import sqlite3
import csv

# Path to my database
DB_PATH = "Championship.db"

# Path to my goals CSV
CSV_PATH = "data/Goals.csv"

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

    # Cleared old data
    cursor.execute("DELETE FROM goals")

    # Inserted new goals data
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