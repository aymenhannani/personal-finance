# pages/3_✏️_Edit_Data.py

import streamlit as st
from data_processing.process_data import load_and_process_data
from pages.widgets.data.data_editor_widget import data_editor_widget
from pages.widgets.sidebar.navigation_widget import go_back_button

st.title("Edit Data")

# Load and process data
data = load_and_process_data()

# Create a data editor
edited_data = data_editor_widget(data)

# Handle the 'Save Changes' button click
if st.button("Save Changes"):
    # Update session state with the modified data
    st.session_state['raw_data'] = edited_data
    # Optionally, save to Excel
    edited_data.to_excel('data_finance.xlsx', index=False)
    st.success("Changes saved successfully!")

# Provide option to go back
go_back_button()
