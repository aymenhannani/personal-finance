# pages/Upload_and_Select_Columns.py

import streamlit as st
from ...widgets.data.file_upload_widget import upload_file_and_select_columns

def app():
    st.title("Upload Your Excel File and Select Columns")

    # Ensure user is logged in using session state and cookies
    if 'is_authenticated' not in st.session_state or not st.session_state['is_authenticated']:
        st.error("Please log in to upload data.")

    # Call the widget to handle file upload and column selection
    upload_file_and_select_columns()

    # Provide option to proceed to the next page if columns are selected
    if 'selected_columns' in st.session_state:
        st.write("You can now proceed to the **Visualization and Filters** page.")
        if st.button("Go to Visualization and Filters"):
            st.experimental_set_query_params(page="2_📊_Visualization_and_Filters.py")
