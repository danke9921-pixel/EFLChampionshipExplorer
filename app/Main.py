# Author: Đani Čolaković
# main.py
# Streamlit interface for login, registration, and admin controls

import streamlit as st
from Login import authenticate, register_user
from admin_page import admin_page
from league_table import league_table_page

def main():
    st.title("EFL Championship Explorer")

    # sidebar menu
    menu = ["Login", "Register", "Admin", "League Table"]
    choice = st.sidebar.selectbox("Menu", menu)

    # LOGIN PAGE
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

                # store user role for admin access
                st.session_state["role"] = user["role"]
                st.session_state["username"] = user["username"]

                st.write(f"Favourite Team: {user['favourite_team']}")
            else:
                st.error("Invalid credentials")

    # REGISTER PAGE
    elif choice == "Register":
        st.subheader("Register")

        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        favourite_team = st.text_input("Favourite Team")

        if st.button("Register"):
            success, message = register_user(new_username, new_password, favourite_team)

            if success:
                st.success("Account created successfully")
            else:
                if message == "username_exists":
                    st.error("Username already exists")
                elif message == "weak_password":
                    st.error("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")

    # ADMIN PAGE
    elif choice == "Admin":
        if "role" in st.session_state and st.session_state["role"] == "admin":
            admin_page()
        else:
            st.error("You do not have permission to access the admin dashboard.")

    # LEAGUE TABLE PAGE
    elif choice == "League Table":
        league_table_page()

if __name__ == "__main__":
    main()