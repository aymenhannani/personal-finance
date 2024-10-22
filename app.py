# streamlit_app.py
import streamlit as st

st.set_page_config(page_title='Excel Data Visualization', layout='wide')

st.title("Welcome to the Excel Data Visualization App")

st.write("""
This app allows you to upload an Excel file, select the relevant columns, and visualize your data interactively.

**Instructions:**

1. Go to **Upload and Select Columns** page to upload your data and specify the columns.
2. Proceed to **Visualization and Filters** page to interact with your data.

Use the navigation on the left to switch between pages.
""")
