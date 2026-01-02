# Author: Đani Čolaković
import sqlite3
import pandas as pd
import os

# DB is in the SAME folder as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Championship.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

matches = pd.read_sql_query("SELECT * FROM matches", conn)

team_names = pd.unique(matches[["home_team", "away_team"]].values.ravel())
teams = pd.DataFrame({"team": team_names})

teams["played"] = 0
teams["won"] = 0
teams["drawn"] = 0
teams["lost"] = 0
teams["goals_for"] = 0
teams["goals_against"] = 0
teams["goal_difference"] = 0
teams["points"] = 0

for _, match in matches.iterrows():
    home = match["home_team"]
    away = match["away_team"]
    hg = match["home_goals"]
    ag = match["away_goals"]

    teams.loc[teams["team"] == home, "played"] += 1
    teams.loc[teams["team"] == away, "played"] += 1

    teams.loc[teams["team"] == home, "goals_for"] += hg
    teams.loc[teams["team"] == home, "goals_against"] += ag
    teams.loc[teams["team"] == away, "goals_for"] += ag
    teams.loc[teams["team"] == away, "goals_against"] += hg

    if hg > ag:
        teams.loc[teams["team"] == home, "won"] += 1
        teams.loc[teams["team"] == away, "lost"] += 1
        teams.loc[teams["team"] == home, "points"] += 3
    elif ag > hg:
        teams.loc[teams["team"] == away, "won"] += 1
        teams.loc[teams["team"] == home, "lost"] += 1
        teams.loc[teams["team"] == away, "points"] += 3
    else:
        teams.loc[teams["team"] == home, "drawn"] += 1
        teams.loc[teams["team"] == away, "drawn"] += 1
        teams.loc[teams["team"] == home, "points"] += 1
        teams.loc[teams["team"] == away, "points"] += 1

teams["goal_difference"] = teams["goals_for"] - teams["goals_against"]
teams = teams.sort_values(by=["points", "goal_difference", "goals_for"], ascending=False)

cur.execute("DROP TABLE IF EXISTS league_table")
cur.execute("""
    CREATE TABLE league_table (
        team TEXT PRIMARY KEY,
        played INTEGER,
        won INTEGER,
        drawn INTEGER,
        lost INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        points INTEGER
    )
""")

for _, row in teams.iterrows():
    cur.execute("""
        INSERT INTO league_table
        (team, played, won, drawn, lost, goals_for, goals_against, goal_difference, points)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["team"],
        int(row["played"]),
        int(row["won"]),
        int(row["drawn"]),
        int(row["lost"]),
        int(row["goals_for"]),
        int(row["goals_against"]),
        int(row["goal_difference"]),
        int(row["points"])
    ))

conn.commit()
conn.close()

print(" League table rebuilt.")