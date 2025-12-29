# Author: Đani Čolaković
import streamlit as st
import pandas as pd
import sqlite3
# Page setup

st.set_page_config(page_title="Top Goalscorers", layout="wide")
st.title("Top Goalscorers")

# Connect to the database and load goal data
conn = sqlite3.connect("Championship.db")
goals_df = pd.read_sql_query("SELECT player, team, type FROM goals", conn)
conn.close()

# Calculate total goals per player
top_scorers = goals_df.groupby(["player", "team"]).size().reset_index(name="goals")
top_scorers = top_scorers.sort_values(by="goals", ascending=False).head(10)

# Count how many times each goal type appears
goal_types = goals_df["type"].value_counts().reset_index()
goal_types.columns = ["type", "count"]

# Display top goalscorers table
st.markdown("### 🏆 Top 10 Goalscorers")
st.dataframe(top_scorers, use_container_width=True)
# Bar chart of goals per player
st.markdown("### 📊 Goals by Player")
st.bar_chart(top_scorers.set_index("player")["goals"])
# Display goal type distribution
st.markdown("### ⚽ Goal Type Distribution")
st.dataframe(goal_types, use_container_width=True)
# Analytical summary section
st.markdown("### 📘 Analytical Commentary")
st.write("""
This dashboard presents a concise overview of individual scoring performance within the EFL Championship dataset.
The top goalscorers are ranked by total goals, offering insight into attacking efficiency across teams.
The goal type breakdown supports tactical analysis, revealing trends in scoring methods such as penalties, headers, and open play.
This page serves as a foundation for further statistical modelling and performance evaluation.
""")