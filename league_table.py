import streamlit as st
import pandas as pd
import sqlite3

# league table page
def league_table_page():
    st.title("Championship League Table")

    # load team data from SQLite
    conn = sqlite3.connect("Championship.db")
    df = pd.read_sql_query("SELECT * FROM league_table ORDER BY points DESC", conn)
    conn.close()

    st.subheader("League Table (Sorted by Points)")
    st.dataframe(df)

    st.subheader("Sort Options")
    sort_choice = st.selectbox(
        "Sort teams by:",
        ["points", "goals_for", "goals_against", "won", "lost"]
    )

    sorted_df = df.sort_values(by=sort_choice, ascending=False)
    st.dataframe(sorted_df)