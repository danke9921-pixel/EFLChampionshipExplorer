import streamlit as st
import sqlite3

# Get all users from the database
def get_all_users():
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("SELECT id, username, role, banned FROM users")
    users = cur.fetchall()
    conn.close()
    return users

# Remove a user from the database
def delete_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Change a user's role to admin
def promote_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Ban a user
def ban_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET banned = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Unban a user
def unban_user(user_id):
    conn = sqlite3.connect("Championship.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET banned = 0 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

# Admin Dashboard Page
def admin_page():
    st.title("Admin Dashboard")

    # Only Admin can access this page
    if "role" not in st.session_state or st.session_state["role"] != "admin":
        st.error("Access denied.")
        st.stop()

    st.subheader("User Management")

    users = get_all_users()

    # Show all users with actions
    for user in users:
        user_id, username, role, banned = user

        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

        col1.write(username)
        col2.write(role)

        # Ban / Unban Buttons
        if username == st.session_state["username"]:
            col3.write("—")  # cannot ban yourself
        else:
            if banned == 1:
                if col3.button("Unban", key=f"unban_{user_id}"):
                    unban_user(user_id)
                    st.experimental_rerun()
            else:
                if col3.button("Ban", key=f"ban_{user_id}"):
                    ban_user(user_id)
                    st.experimental_rerun()

        # promote button
        if role == "admin":
            col4.write("—")  # already admin
        else:
            if col4.button("Promote", key=f"promote_{user_id}"):
                promote_user(user_id)
                st.experimental_rerun()

        # delete button (with confirmation)
        if username == st.session_state["username"]:
            col5.write("—")  # cannot delete yourself
        else:
            if col5.button("Delete", key=f"delete_{user_id}"):
                st.session_state["confirm_delete"] = user_id
                st.experimental_rerun()

    # delete confirmation popup
    if "confirm_delete" in st.session_state:
        st.warning("Are you sure you want to delete this user?")
        colA, colB = st.columns(2)

        if colA.button("Yes, delete"):
            delete_user(st.session_state["confirm_delete"])
            del st.session_state["confirm_delete"]
            st.experimental_rerun()

        if colB.button("Cancel"):
            del st.session_state["confirm_delete"]
            st.experimental_rerun()