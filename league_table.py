import streamlit as st
import pandas as pd

# league table page
def league_table_page():
    st.title("Championship League Table")

    # load team data
    try:
        df = pd.read_csv("data/Teams.csv")
    except FileNotFoundError:
        st.error("Teams.csv not found in the data folder.")
        return

    st.subheader("Team Data")
    st.dataframe(df)

    st.subheader("League Table (Sorted by Points)")
    table = df.sort_values(by="Points", ascending=False)
    table.index = range(1, len(table) + 1)
    st.dataframe(table)

    st.subheader("Sort Options")
    sort_choice = st.selectbox(
        "Sort teams by:",
        ["Points", "Goals Scored", "Goals Conceded", "Wins", "Losses"]
    )

    sorted_table = df.sort_values(by=sort_choice, ascending=False)
    sorted_table.index = range(1, len(sorted_table) + 1)
    st.dataframe(sorted_table)