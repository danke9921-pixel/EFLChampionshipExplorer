# Author: Đani Čolaković
# app.py
# Streamlit interface for login, registration, and page switching

import streamlit as st
from Login import authenticate, register_user   # backend login functions

def main():
    st.title("EFL Championship Explorer")

    # Sidebar navigation
    menu = ["Login", "Register", "Admin", "Analytics", "League Table", "Matchday Results", "Top Goalscorers"]
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
            st.switch_page("pages/admin_page.py")
        else:
            st.error("You do not have permission to access the admin dashboard.")

    # ANALYTICS PAGE
    elif choice == "Analytics":
        st.switch_page("pages/analytics.py")

    # LEAGUE TABLE PAGE
    elif choice == "League Table":
        st.switch_page("pages/league_table.py")

    # MATCHDAY RESULTS PAGE
    elif choice == "Matchday Results":
        st.switch_page("pages/Matchday_Results.py")

    # TOP GOALSCORERS PAGE
    elif choice == "Top Goalscorers":
        st.switch_page("pages/Top_Goalscorers.py")


if __name__ == "__main__":
    main()