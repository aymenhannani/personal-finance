# widgets/auth.py

import streamlit as st

def get_current_user_id():
    # Retrieve the current user's ID from session state
    return st.session_state.get("user_id")
