# Author: Đani Čolaković
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="League Table", layout="wide")
st.title("League Table")

# Load league table data
conn = sqlite3.connect("Championship.db")
df = pd.read_sql_query("SELECT * FROM league_table", conn)
conn.close()

# Sort by points and goal difference
df = df.sort_values(by=["points", "goal_difference"], ascending=False)

st.markdown("### 📊 Current Standings")
st.dataframe(df, use_container_width=True)

st.markdown("""
### 📘 Analytical Commentary

This league table summarises team performance across the season,
highlighting wins, draws, losses, and goal metrics. Sorting by points
and goal difference provides a clear competitive hierarchy and helps
identify trends in consistency, attacking strength, and defensive stability.
""")