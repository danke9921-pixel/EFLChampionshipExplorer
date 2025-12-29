# Author: Đani Čolaković
import streamlit as st
import sqlite3
import pandas as pd

# Load match data from the database
def load_matches():
    conn = sqlite3.connect("Championship.db")
    df = pd.read_sql_query("SELECT * FROM matches", conn)
    conn.close()
    return df

# Main Page Execution

st.set_page_config(page_title="Team Analytics", layout="wide")
st.title("Team analytics")

df = load_matches()
# Ensure required columns exist before processing
expected = ["home_team", "away_team", "home_goals", "away_goals"]
missing = [col for col in expected if col not in df.columns]
if missing:
    st.error(f"missing columns: {', '.join(missing)}")
    st.stop()
# This builds a list of all teams in the dataset
teams = sorted(set(df["home_team"].unique()) | set(df["away_team"].unique()))
team = st.selectbox("select a team", teams)
# Filter matches where the selected team played
team_matches = df[(df["home_team"] == team) | (df["away_team"] == team)]

st.subheader(f"Basic stats for {team}")
st.write("Total matches:", len(team_matches))
# Initialise statistics
goals_scored = 0
goals_conceded = 0
wins = draws = losses = 0
form = []

# Calculate stats by match 
for _, row in team_matches.iterrows():
    if row["home_team"] == team:
# Team played at home 
        goals_scored += row["home_goals"]
        goals_conceded += row["away_goals"]
        if row["home_goals"] > row["away_goals"]:
            wins += 1
            form.append("W")
        elif row["home_goals"] == row["away_goals"]:
            draws += 1
            form.append("D")
        else:
            losses += 1
            form.append("L")
    # Team played away
    else:
        goals_scored += row["away_goals"]
        goals_conceded += row["home_goals"]
        if row["away_goals"] > row["home_goals"]:
            wins += 1
            form.append("W")
        elif row["away_goals"] == row["home_goals"]:
            draws += 1
            form.append("D")
        else:
            losses += 1
            form.append("L")
# Show calculated statistics from EFL Championship Teams
st.write("Goals scored:", goals_scored)
st.write("Goals conceded:", goals_conceded)
st.write("Wins:", wins)
st.write("Draws:", draws)
st.write("Losses:", losses)

st.markdown("---")
st.subheader("Last 5 matches")
st.write("Form:", " - ".join(form[-5:]))

st.markdown("---")
st.subheader("Goal trend")
st.line_chart(team_matches["home_goals"])