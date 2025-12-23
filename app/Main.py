# Author: Đani Čolaković
# main.py
# Streamlit interface for login, registration, and admin controls

import streamlit as st
from Login import authenticate, register_user

def main():
    st.title("EFL Championship Explorer")

    menu = ["Login", "Register", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = authenticate(username, password)

            if user == "banned":
                st.error("Your account has been banned.")
            elif user:
                st.success(f"Welcome {user['username']}!")
                st.write(f"Favourite Team: {user['favourite_team']}")
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.subheader("Register")

        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        favourite_team = st.text_input("Favourite Team")

        if st.button("Register"):
            success = register_user(new_username, new_password, favourite_team)
            if success:
                st.success("Account created successfully")
            else:
                st.error("Username already exists")

    elif choice == "Admin":
        st.subheader("Admin Panel")

        admin_user = st.text_input("Admin Username")
        admin_pass = st.text_input("Admin Password", type="password")

        if admin_user == "admin" and admin_pass == "admin123":
            st.success("Admin logged in")

            from database.connect import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT username, banned FROM users")
            users = cursor.fetchall()

            st.write("### User Management")

            for u in users:
                username = u["username"]
                banned = u["banned"]

                st.write(f"User: **{username}** | Banned: **{banned}**")

                col1, col2 = st.columns(2)

                if banned == 0:
                    if col1.button(f"Ban {username}"):
                        cursor.execute("UPDATE users SET banned = 1 WHERE username = ?", (username,))
                        conn.commit()
                        st.success(f"{username} has been banned")
                else:
                    if col2.button(f"Unban {username}"):
                        cursor.execute("UPDATE users SET banned = 0 WHERE username = ?", (username,))
                        conn.commit()
                        st.success(f"{username} has been unbanned")

            conn.close()
        else:
            st.info("Enter admin credentials to continue.")

if __name__ == "__main__":
    main()