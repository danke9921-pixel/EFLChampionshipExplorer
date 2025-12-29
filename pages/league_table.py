# Author: Đani Čolaković
import streamlit as st
import pandas as pd
import sqlite3
# Page setup 
st.set_page_config(page_title="League Table", layout="wide")
st.title("League Table")

# Load league table data from the database
conn = sqlite3.connect("Championship.db")
df = pd.read_sql_query("SELECT * FROM league_table", conn)
conn.close()

# Sort teams by points first, then goal difference
df = df.sort_values(by=["points", "goal_difference"], ascending=False)

# Display the EFL Championship standings
st.markdown("### 📊 Current Standings")
st.dataframe(df, use_container_width=True)

# Analytical summary section
st.markdown("""
### 📘 Analytical Commentary

This league table provides a structured overview of team performance across the season,  
summarising key indicators such as matches played, wins, draws, losses, and goal metrics.  
Sorting by points and goal difference offers a clear representation of competitive hierarchy,  
highlighting both consistency and attacking/defensive efficiency.

From an analytical perspective, this table supports longitudinal performance tracking,  
benchmarking between teams, and the identification of emerging trends that may influence  
future match outcomes or tactical adjustments.
""")