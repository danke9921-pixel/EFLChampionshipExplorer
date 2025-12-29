# Author: Đani Čolaković
# Script for importing player data from CSV into the SQLite Database 
import sqlite3
import csv
import os

# Path to the SQLite Database 
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Championship.db")

# Path to the CSV file containing EFL Championshipplayer data
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "team_players.csv")

# Opens a connection to the database. 
# Returns the connection object or exists on failure.
def connect_db():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        exit(1)

# Validates a single CSV row to ensure it contains the correct number of fields and valid player data.
def validate_row(row):
    if len(row) != 4:
        return False

    club, name, position, nationality = row

    if not club.strip():
        return False
    if not name.strip():
        return False
    if position not in ("GK", "DEF", "MID", "FWD"):
        return False
    if not nationality.strip():
        return False

    return True

# Imports players from the CSV file into the Players Table
def import_players():
    conn = connect_db()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if not validate_row(row):
                    skipped += 1
                    continue

                cursor.execute(
                    "INSERT INTO Players (club, name, position, nationality) VALUES (?, ?, ?, ?)",
                    row
                )
                inserted += 1

        conn.commit()

    except FileNotFoundError:
        print(f"CSV file not found: {CSV_PATH}")
        exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

    finally:
        conn.close()

    print("Player import completed.")
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    import_players()