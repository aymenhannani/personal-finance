# streamlit_app.py

import streamlit as st
st.set_page_config(page_title='Excel Data Visualization', layout='wide')

from streamlit_cookies_manager import EncryptedCookieManager

# Set page configuration first

# Replace "your_secure_password" with a strong password of your choice.
cookies = EncryptedCookieManager(
    prefix="my_app",
    password="12345"
)

# Ensure the cookies manager is ready before continuing
if not cookies.ready():
    # Wait for the cookies manager to initialize
    st.stop()

# Save authenticated state into the cookies
if st.session_state.get('is_authenticated', False):
    cookies['is_authenticated'] = 'true'
    cookies['authenticated_user_id'] = str(st.session_state['authenticated_user_id'])
    cookies.save()

# Set the title and instructions
st.title("Welcome to the Excel Data Visualization App")

st.write("""
This app allows you to upload an Excel file, select the relevant columns, and visualize your data interactively.

**Instructions:**

1. Go to **Upload and Select Columns** page to upload your data and specify the columns.
2. Proceed to **Visualization and Filters** page to interact with your data.

Use the navigation on the left to switch between pages.
""")
