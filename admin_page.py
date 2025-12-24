import streamlit as st
import sqlite3

# get all users from the database
def get_all_users():
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users")
    users = cur.fetchall()
    conn.close()
    return users

# remove a user from the database
def delete_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# change a user's role to admin
def promote_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# admin dashboard page
def admin_page():
    st.title("Admin Dashboard")

    # only admins can access this page
    if "role" not in st.session_state or st.session_state["role"] != "admin":
        st.error("Access denied.")
        st.stop()

    st.subheader("User Management")

    users = get_all_users()

    # show all users with actions
    for user in users:
        user_id, username, role = user

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        col1.write(username)
        col2.write(role)

        if col3.button("Delete", key=f"delete_{user_id}"):
            delete_user(user_id)
            st.experimental_rerun()

        if col4.button("Promote", key=f"promote_{user_id}"):
            promote_user(user_id)
            st.experimental_rerun()