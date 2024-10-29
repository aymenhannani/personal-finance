# data_processing/data_loader.py

import streamlit as st
from data_processing.process_data import process_data

def load_and_process_data():
    if 'raw_data' in st.session_state and 'selected_columns' in st.session_state:
        # Process data using the external function
        data = process_data(st.session_state['raw_data'], st.session_state['selected_columns'])
        return data
    else:
        st.error("No data available. Please go back to **Upload and Select Columns** page.")
        if st.button("Go Back to Upload and Select Columns"):
            st.experimental_set_query_params(page="1_📂_Upload_and_Select_Columns.py")
        st.stop()
