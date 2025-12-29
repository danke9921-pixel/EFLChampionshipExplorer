import streamlit as st
import sqlite3
import os

# Build correct database path (root folder)
def get_db():
    return os.path.join(os.path.dirname(__file__), "..", "Championship.db")

# Load all users from the database
def get_all_users():
    try:
        conn = sqlite3.connect(get_db())
        cur = conn.cursor()
        cur.execute("SELECT id, username, role, banned FROM users")
        users = cur.fetchall()
        return users
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return []
    finally:
        conn.close()

# Delete a user from the database
def delete_user(user_id):
    try:
        conn = sqlite3.connect(get_db())
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        st.error(f"Error deleting user: {e}")
    finally:
        conn.close()

# Promote a user to admin
def promote_user(user_id):
    try:
        conn = sqlite3.connect(get_db())
        cur = conn.cursor()
        cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        st.error(f"Error promoting user: {e}")
    finally:
        conn.close()

# Ban a user
def ban_user(user_id):
    try:
        conn = sqlite3.connect(get_db())
        cur = conn.cursor()
        cur.execute("UPDATE users SET banned = 1 WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        st.error(f"Error banning user: {e}")
    finally:
        conn.close()

# Unban a user
def unban_user(user_id):
    try:
        conn = sqlite3.connect(get_db())
        cur = conn.cursor()
        cur.execute("UPDATE users SET banned = 0 WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        st.error(f"Error unbanning user: {e}")
    finally:
        conn.close()

# 🔥 MAIN PAGE EXECUTION (no function)
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("Admin Dashboard")

# Only admins can access this page
if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("Access denied.")
    st.stop()

st.subheader("User Management")

users = get_all_users()

# Display all users with action buttons
for user in users:
    user_id, username, role, banned = user

    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

    col1.write(username)
    col2.write(role)

    # Ban / Unban buttons
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

    # Promote button
    if role == "admin":
        col4.write("—")  # already admin
    else:
        if col4.button("Promote", key=f"promote_{user_id}"):
            promote_user(user_id)
            st.experimental_rerun()

    # Delete button (with confirmation)
    if username == st.session_state["username"]:
        col5.write("—")  # cannot delete yourself
    else:
        if col5.button("Delete", key=f"delete_{user_id}"):
            st.session_state["confirm_delete"] = user_id
            st.experimental_rerun()

    st.markdown("---")  # visual separator

# Delete confirmation popup
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