# Author: Đani Čolaković
import streamlit as st
import pandas as pd
import sqlite3
# Page setup 

st.set_page_config(page_title="Matchday Results", layout="wide")
st.title("Matchday Results")

# Load match data from the database
conn = sqlite3.connect("Championship.db")
df = pd.read_sql_query("SELECT * FROM matches ORDER BY matchday, date", conn)
conn.close()

# Here is a list of available matchdays from the dropdown menu 
matchdays = sorted(df["matchday"].unique())
selected = st.selectbox("Select Matchday", matchdays)

# Filter results for the selected matchday
filtered = df[df["matchday"] == selected]
# Show matchday results 
st.markdown(f"### ⚽ Results for Matchday {selected}")
st.dataframe(filtered, use_container_width=True)

# Analytical summary section 
st.markdown("""
### 📘 Analytical Commentary

This page displays fixture outcomes for a selected matchday, enabling chronological review of team performance.  
By filtering results per round, users can identify trends, momentum shifts, and key turning points in the season.  
This structure supports tactical retrospectives, player impact analysis, and matchday-level scouting insights.
""")