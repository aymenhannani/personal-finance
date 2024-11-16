# app.py

import streamlit as st
st.set_page_config(page_title='Excel Data Visualization', layout='wide')

from streamlit_cookies_manager import EncryptedCookieManager

# Import the navigation module
from webapp.navigation import navigation

# Import your page modules
from webapp.pages.authentication import User_Authentication,User_Login


from webapp.pages.data_management import Upload_and_Select_Columns, Edit_Data
from webapp.pages.budget import Create_Edit_Budget, Budget_View
from webapp.pages.summary import Ongoing_Month_Summary, Monthly_Summary
from webapp.pages.visualization import Visualization_and_Filters
# At the top of app.py
if 'is_authenticated' not in st.session_state:
    st.session_state['is_authenticated'] = False

# Set up cookies for authentication
cookies = EncryptedCookieManager(
    prefix="my_app",
    password="12345"
)

# Ensure the cookies manager is ready before continuing
if not cookies.ready():
    # Wait for the cookies manager to initialize
    st.stop()



# Define the PAGES dictionary, including your welcome page
PAGES = {
    "Home": {
        "🏠 Welcome": None  # We'll handle the welcome page separately
    },
    "Authentication": {
        "🔐 User Authentication": User_Authentication,
        "🔑 User Login": User_Login
    },
    "Data Management": {
        "📂 Upload and Select Columns": Upload_and_Select_Columns,
        "📝 Edit Data": Edit_Data
    },
    "Budget": {
        "✏️ Create/Edit Budget": Create_Edit_Budget,
        "📅 Budget View": Budget_View
    },
    "Summary": {
        "📅 Ongoing Month Summary": Ongoing_Month_Summary,
        "📅 Monthly Summary": Monthly_Summary
    },
    "Visualization": {
        "📊 Visualization and Filters": Visualization_and_Filters
    }
}

# Use the navigation module to get the selected section and page
section, page = navigation.main_menu(PAGES)

# Display the selected page
if section == "Home" and page == "🏠 Welcome" :
    # Your original welcome content
    st.title("Welcome to the Excel Data Visualization App")

    st.write("""
    This app allows you to upload an Excel file, select the relevant columns, and visualize your data interactively.

    **Instructions:**

    1. Go to **Upload and Select Columns** page to upload your data and specify the columns.
    2. Proceed to **Visualization and Filters** page to interact with your data.

    Use the navigation on the left to switch between pages.
    """)
else :
    # Call the app() function of the selected page module
    PAGES[section][page].app()
