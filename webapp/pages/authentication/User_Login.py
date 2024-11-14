# pages/1_🔑_User_Login.py

import streamlit as st
from database.auth_utils import authenticate_user

def app():
    st.title("🔑 User Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if username and password:
            # Authenticate user here
            user = authenticate_user(username, password)

            if user:
                st.session_state['authenticated_user_id'] = user.id
                st.session_state['authenticated_username'] = user.username
                st.session_state['is_authenticated'] = True
                st.success(f"Welcome {user.username}!")
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")
