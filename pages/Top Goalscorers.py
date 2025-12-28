import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Top Goalscorers", layout="wide")
st.title("Top Goalscorers")

# Connect to DB
conn = sqlite3.connect("Championship.db")
goals_df = pd.read_sql_query("SELECT player, team, type FROM goals", conn)
conn.close()

# Aggregate goals
top_scorers = goals_df.groupby(["player", "team"]).size().reset_index(name="goals")
top_scorers = top_scorers.sort_values(by="goals", ascending=False).head(10)

# Goal type distribution
goal_types = goals_df["type"].value_counts().reset_index()
goal_types.columns = ["type", "count"]

# Layout
st.markdown("### 🏆 Top 10 Goalscorers")
st.dataframe(top_scorers, use_container_width=True)

st.markdown("### 📊 Goals by Player")
st.bar_chart(top_scorers.set_index("player")["goals"])

st.markdown("### ⚽ Goal Type Distribution")
st.dataframe(goal_types, use_container_width=True)

st.markdown("### 📘 Analytical Commentary")
st.write("""
This dashboard presents a concise overview of individual scoring performance within the EFL Championship dataset.
The top goalscorers are ranked by total goals, offering insight into attacking efficiency across teams.
The goal type breakdown supports tactical analysis, revealing trends in scoring methods such as penalties, headers, and open play.
This page serves as a foundation for further statistical modelling and performance evaluation.
""")