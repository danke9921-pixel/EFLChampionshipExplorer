import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Matchday Results", layout="wide")
st.title("Matchday Results")

# Connect to DB
conn = sqlite3.connect("Championship.db")
df = pd.read_sql_query("SELECT * FROM matches ORDER BY matchday, date", conn)
conn.close()

# Matchday selector
matchdays = sorted(df["matchday"].unique())
selected = st.selectbox("Select Matchday", matchdays)

# Filter and display
filtered = df[df["matchday"] == selected]
st.markdown(f"### ⚽ Results for Matchday {selected}")
st.dataframe(filtered, use_container_width=True)

# Academic summary
st.markdown("""
### 📘 Analytical Commentary

This page displays fixture outcomes for a selected matchday, enabling chronological review of team performance.  
By filtering results per round, users can identify trends, momentum shifts, and key turning points in the season.  
This structure supports tactical retrospectives, player impact analysis, and matchday-level scouting insights.
""")