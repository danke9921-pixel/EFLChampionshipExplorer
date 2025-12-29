# Author: Đani Čolaković
# app.py
# Main Streamlit interface for Login, Registration and Page Navigation

import streamlit as st
from Login import authenticate, register_user   # Backend functions for Login + Registration 

def main():
    st.title("EFL Championship Explorer")

    # Sidebar Navigation Menu for switching between pages
    menu = ["Login", "Register", "Admin", "Analytics", "League Table", "Matchday Results", "Top Goalscorers"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Login Page
    if choice == "Login":
        st.subheader("Login")
        # User Input Fields for username and password
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        # Handle login attempt 
        if st.button("Login"):
            user = authenticate(username, password)
            # Check different login outcomes
            if user == "banned":
                st.error("Your account has been banned.")
            elif user:
                st.success(f"Welcome {user['username']}!")
                # Store user info in session for access control 
                st.session_state["role"] = user["role"]
                st.session_state["username"] = user["username"]

                st.write(f"Favourite Team: {user['favourite_team']}")
            else:
                st.error("Invalid credentials")

    # Registration Page
    elif choice == "Register":
        st.subheader("Register")
       # Registration Input Fields 
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        favourite_team = st.text_input("Favourite Team")
        # Handle Registration Attempt 
        if st.button("Register"):
            success, message = register_user(new_username, new_password, favourite_team)

            if success:
                st.success("Account created successfully")
            else:
                 # Handle specific registration errors
                if message == "username_exists":
                    st.error("Username already exists")
                elif message == "weak_password":
                    st.error("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.")

    # Admin Page (Restricted Access)
    elif choice == "Admin":
        # Only admin users can access this page 
        if "role" in st.session_state and st.session_state["role"] == "admin":
            st.switch_page("pages/admin_page.py")
        else:
            st.error("You do not have permission to access the admin dashboard.")
 
    # Other Pages Navigation 

    elif choice == "Analytics":
        st.switch_page("pages/analytics.py")

    elif choice == "League Table":
        st.switch_page("pages/league_table.py")

    elif choice == "Matchday Results":
        st.switch_page("pages/Matchday_Results.py")

    elif choice == "Top Goalscorers":
        st.switch_page("pages/Top_Goalscorers.py")


if __name__ == "__main__":
    main()