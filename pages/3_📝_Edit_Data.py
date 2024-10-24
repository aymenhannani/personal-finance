# pages/3_✏️_Edit_Data.py

import streamlit as st
import pandas as pd
from data_processing.process_data import process_data

st.title("Edit Data")

# Check if raw data and selected columns are available
if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
    # Process data using the external function
    data = process_data(st.session_state['raw_data'], st.session_state['selected_columns'])

    # Create a data editor
    edited_data = st.data_editor(data=data, num_rows="dynamic", hide_index=True, key='new_data')

    # Handle the 'Save Changes' button click
    if st.button("Save Changes"):
        # Handle added, edited, and deleted rows as before...
        # Update session state with the modified data
        st.session_state['raw_data'] = edited_data
        # Optionally, save to Excel
        edited_data.to_excel('data_finance.xlsx', index=False)
        st.success("Changes saved successfully!")
else:
    st.warning("Upload data and set column selections to proceed.")
