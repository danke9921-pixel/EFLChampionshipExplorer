import sqlite3

DB_PATH = "Championship.db"

def create_players_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club TEXT NOT NULL,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                nationality TEXT NOT NULL
            );
        """)

        conn.commit()
        conn.close()
        print("Players table created successfully.")

    except Exception as e:
        print(f"Error creating table: {e}")

if __name__ == "__main__":
    create_players_table()