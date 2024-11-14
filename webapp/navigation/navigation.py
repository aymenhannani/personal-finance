# navigation/navigation.py

import streamlit as st

def main_menu(PAGES):
    st.sidebar.title("Navigation")

    # Select Section
    section = st.sidebar.selectbox("Section", list(PAGES.keys()))

    # Select Page within Section
    page = st.sidebar.radio("Page", list(PAGES[section].keys()))

    return section, page
