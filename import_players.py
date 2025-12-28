import sqlite3
import csv
import os

DB_PATH = "Championship.db"
CSV_PATH = os.path.join("data", "team_players.csv")


def connect_db():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        exit(1)


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